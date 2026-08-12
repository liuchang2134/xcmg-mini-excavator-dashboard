from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE


ROOT = Path(__file__).resolve().parents[1]
CONFLICTS_PATH = ROOT / "crane-image-conflicts.json"
DECISIONS_PATH = ROOT / "data" / "crane-ppt-insights" / "image-ownership.json"
SOURCE_DIR = ROOT / "assets" / "crane-ppt-source"
PRESENTATION_DIR = ROOT / "data" / "source-presentations"


def _iter_pictures(shapes: Iterable[Any]) -> Iterable[Any]:
    for shape in shapes:
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from _iter_pictures(shape.shapes)
        elif shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            yield shape


def _presentation_image_pages(presentation: Path) -> dict[str, list[int]]:
    pages: dict[str, set[int]] = defaultdict(set)
    deck = Presentation(str(presentation))
    for slide_number, slide in enumerate(deck.slides, 1):
        for picture in _iter_pictures(slide.shapes):
            digest = hashlib.md5(picture.image.blob).hexdigest()
            pages[digest].add(slide_number)
    return {digest: sorted(values) for digest, values in pages.items()}


def _slide_number(path: str) -> int:
    match = re.search(r"(?:^|/)s(\d+)-", path.replace("\\", "/"))
    if not match:
        raise ValueError(f"Cannot read slide number from {path}")
    return int(match.group(1))


def _source_asset(path: str) -> str:
    candidate = ROOT / path
    if "crane-ppt-source" in candidate.as_posix() and candidate.exists():
        return candidate.relative_to(ROOT).as_posix()
    stem = candidate.stem
    matches = sorted(SOURCE_DIR.glob(f"{stem}.*"))
    if len(matches) != 1:
        raise ValueError(f"Expected one source asset for {path}; found {len(matches)}")
    return matches[0].relative_to(ROOT).as_posix()


def _topic(usages: list[dict[str, str]]) -> tuple[str, str]:
    captions = " ".join(item.get("caption", "") for item in usages)
    if "客户使用评价" in captions:
        return "客户使用评价影像", "Customer evaluation image"
    if "市场与工况" in captions:
        return "区域施工场景影像", "Regional jobsite image"
    return "产品改进支撑影像", "Product improvement reference image"


def adjudicate() -> dict[str, Any]:
    conflicts = json.loads(CONFLICTS_PATH.read_text(encoding="utf-8"))
    presentations = sorted(PRESENTATION_DIR.glob("*.pptx"))
    if len(presentations) != 1:
        raise FileNotFoundError(
            f"Expected one source presentation in {PRESENTATION_DIR}; found {len(presentations)}"
        )
    presentation = presentations[0]
    ppt_pages = _presentation_image_pages(presentation)
    decisions = []
    assets: dict[str, dict[str, Any]] = {}

    for index, conflict in enumerate(conflicts, 1):
        source_assets = sorted({_source_asset(path) for path in conflict["files"]})
        source_digests = {
            hashlib.md5((ROOT / path).read_bytes()).hexdigest() for path in source_assets
        }
        relevant_pages = sorted({_slide_number(path) for path in source_assets})
        confirmed_pages = sorted(
            {
                page
                for digest in source_digests
                for page in ppt_pages.get(digest, [])
                if page in relevant_pages
            }
        )
        if set(confirmed_pages) != set(relevant_pages):
            raise ValueError(
                f"Conflict {index} is not confirmed as exact PPT reuse: "
                f"expected pages {relevant_pages}, confirmed {confirmed_pages}"
            )

        caption_zh, caption_en = _topic(conflict["usages"])
        pages_zh = "、".join(str(page) for page in relevant_pages)
        pages_en = ", ".join(str(page) for page in relevant_pages)
        decision = {
            "id": f"reuse-{index:02d}",
            "content_hash": conflict["hash"],
            "decision": "SOURCE_REUSE",
            "confidence": 1.0,
            "source_slides": relevant_pages,
            "caption_zh": caption_zh,
            "caption_en": caption_en,
            "reason_zh": f"PPT 原始文件在第 {pages_zh} 页复用了完全相同的图片二进制，不能据此判断唯一机型或区域。",
            "reason_en": f"The source presentation reuses the exact same image binary on slides {pages_en}; it cannot establish a unique model or region.",
            "source_assets": source_assets,
            "usages": conflict["usages"],
        }
        decisions.append(decision)
        for asset in source_assets:
            assets[asset] = {
                "decision_id": decision["id"],
                "decision": decision["decision"],
                "source_slides": relevant_pages,
                "caption_zh": caption_zh,
                "caption_en": caption_en,
            }

    payload = {
        "source_presentation": presentation.relative_to(ROOT).as_posix(),
        "method": "Exact binary-image reuse verified inside the source PPTX; no model or region inferred from filenames.",
        "decision_count": len(decisions),
        "decisions": decisions,
        "assets": assets,
    }
    DECISIONS_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return payload


if __name__ == "__main__":
    result = adjudicate()
    print(
        f"Auto-adjudicated {result['decision_count']} conflict groups as verified source reuse; "
        f"wrote {DECISIONS_PATH.relative_to(ROOT)}"
    )
