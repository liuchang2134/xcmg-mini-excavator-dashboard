from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "crane-ppt-insights"
SOURCE_DIR = ROOT / "assets" / "crane-ppt-source"
DISPLAY_DIR = ROOT / "assets" / "crane-ppt-display"


def _asset_order(path: str) -> tuple[int, int, str]:
    match = re.search(r"(?:^|/)s(\d+)-image-(\d+)-", path.replace("\\", "/"))
    if not match:
        return (10**9, 10**9, path)
    return (int(match.group(1)), int(match.group(2)), path)


def _digest(path: str) -> str:
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()


def _canonical_map(records: list[dict[str, Any]]) -> tuple[dict[str, str], list[list[str]]]:
    paths = sorted(
        {
            str(path)
            for record in records
            for path in (record.get("images") or [])
            if (ROOT / str(path)).exists()
        },
        key=_asset_order,
    )
    groups: dict[str, list[str]] = defaultdict(list)
    for path in paths:
        groups[_digest(path)].append(path)

    replacements: dict[str, str] = {}
    duplicates: list[list[str]] = []
    for group in groups.values():
        ordered = sorted(group, key=_asset_order)
        canonical = ordered[0]
        for path in ordered:
            replacements[path] = canonical
        if len(ordered) > 1:
            duplicates.append(ordered)
    return replacements, duplicates


def _replace_images(items: list[str], replacements: dict[str, str]) -> list[str]:
    return list(dict.fromkeys(replacements.get(str(path), str(path)) for path in items))


def _update_image_display(
    referenced: set[str], replacements: dict[str, str], delete_files: bool
) -> int:
    path = DATA_DIR / "image-display.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    original = {str(key): str(value) for key, value in payload.get("images", {}).items()}
    images: dict[str, str] = {}
    for source in sorted(referenced, key=_asset_order):
        candidates = [
            old_source
            for old_source, canonical in replacements.items()
            if canonical == source and old_source in original
        ]
        selected = min(candidates, key=_asset_order) if candidates else source
        if selected in original:
            images[source] = original[selected]

    keep_display = set(images.values())
    if delete_files:
        for candidate in DISPLAY_DIR.glob("*"):
            relative = candidate.relative_to(ROOT).as_posix()
            if candidate.is_file() and relative not in keep_display:
                candidate.unlink()

    payload["image_count"] = len(images)
    payload["images"] = images
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(images)


def _update_image_ownership(replacements: dict[str, str]) -> None:
    path = DATA_DIR / "image-ownership.json"
    if not path.exists():
        return
    payload = json.loads(path.read_text(encoding="utf-8"))
    assets: dict[str, dict[str, Any]] = {}
    for source, metadata in payload.get("assets", {}).items():
        canonical = replacements.get(str(source), str(source))
        existing = assets.get(canonical)
        if existing:
            existing["source_slides"] = sorted(
                {
                    *existing.get("source_slides", []),
                    *metadata.get("source_slides", []),
                }
            )
        else:
            assets[canonical] = dict(metadata)

    for decision in payload.get("decisions", []):
        decision["source_assets"] = _replace_images(
            [str(value) for value in decision.get("source_assets", [])], replacements
        )
    payload["assets"] = assets
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def deduplicate(
    records: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    *,
    update_manifests: bool,
    delete_files: bool,
) -> dict[str, Any]:
    replacements, duplicate_groups = _canonical_map(records)
    for record in records:
        record["images"] = _replace_images(record.get("images") or [], replacements)
    for item in evidence:
        item["assets"] = _replace_images(item.get("assets") or [], replacements)

    referenced = {
        str(path) for record in records for path in (record.get("images") or [])
    }
    removed = sorted(
        {path for path, canonical in replacements.items() if path != canonical},
        key=_asset_order,
    )
    if delete_files:
        for path in removed:
            candidate = ROOT / path
            if candidate.exists():
                candidate.unlink()

    display_count = None
    if update_manifests:
        display_count = _update_image_display(referenced, replacements, delete_files)
        _update_image_ownership(replacements)

    return {
        "duplicate_groups": len(duplicate_groups),
        "removed_files": len(removed),
        "unique_assets": len(referenced),
        "display_assets": display_count,
        "replacement_map": replacements,
    }


def main() -> None:
    slides_path = DATA_DIR / "slides.json"
    evidence_path = DATA_DIR / "evidence.json"
    source_path = DATA_DIR / "source.json"
    records = json.loads(slides_path.read_text(encoding="utf-8"))
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    result = deduplicate(
        records, evidence, update_manifests=True, delete_files=True
    )
    slides_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source["generated_assets"] = result["unique_assets"]
    source["deduplicated_groups"] = result["duplicate_groups"]
    source["deduplicated_files"] = result["removed_files"]
    source_path.write_text(json.dumps(source, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "replacement_map"}, indent=2))


if __name__ == "__main__":
    main()
