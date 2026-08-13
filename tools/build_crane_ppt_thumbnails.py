from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageOps

try:
    from .crane_ppt_render import IMAGE_DISPLAY_MAP, _preferred_image_asset
except ImportError:
    from crane_ppt_render import IMAGE_DISPLAY_MAP, _preferred_image_asset


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets" / "crane-ppt-source"
THUMB_DIR = ROOT / "assets" / "crane-ppt-thumbs"
MANIFEST = ROOT / "data" / "crane-ppt-insights" / "image-thumbnails.json"
SOURCE_LONG_EDGE = 2000
THUMB_LONG_EDGE = 600


def _resize_source_if_needed(path: Path) -> bool:
    with Image.open(path) as opened:
        opened.load()
        image = ImageOps.exif_transpose(opened)
        if max(image.size) <= 2200:
            return False
        image.thumbnail((SOURCE_LONG_EDGE, SOURCE_LONG_EDGE), Image.Resampling.LANCZOS)
        suffix = path.suffix.lower()
        if suffix in {".jpg", ".jpeg"}:
            image.convert("RGB").save(path, quality=82, optimize=True, progressive=True)
        elif suffix == ".webp":
            image.save(path, "WEBP", quality=82, method=6)
        else:
            image.save(path, optimize=True)
    return True


def build() -> dict[str, object]:
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    source_paths = sorted(path for path in SOURCE_DIR.iterdir() if path.is_file())
    resized_sources = sum(_resize_source_if_needed(path) for path in source_paths)

    images: dict[str, str] = {}
    for source_path in source_paths:
        relative_source = source_path.relative_to(ROOT).as_posix()
        preferred_path, _size, _mode = _preferred_image_asset(relative_source)
        input_path = ROOT / preferred_path
        output_path = THUMB_DIR / f"{source_path.stem}-thumb.webp"
        with Image.open(input_path) as opened:
            opened.load()
            image = ImageOps.exif_transpose(opened)
            if image.mode not in {"RGB", "RGBA"}:
                image = image.convert("RGB")
            image.thumbnail((THUMB_LONG_EDGE, THUMB_LONG_EDGE), Image.Resampling.LANCZOS)
            image.save(output_path, "WEBP", quality=82, method=6, exact=True)
        images[relative_source] = output_path.relative_to(ROOT).as_posix()

    manifest = {
        "thumbnail_long_edge": THUMB_LONG_EDGE,
        "quality": 82,
        "source_count": len(source_paths),
        "resized_sources": resized_sources,
        "images": images,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


if __name__ == "__main__":
    result = build()
    print(f"Generated {result['source_count']} crane thumbnails; resized {result['resized_sources']} sources")
