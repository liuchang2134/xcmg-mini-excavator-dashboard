from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets" / "crane-ppt-source"


def resize_oversized_images(
    directory: Path = SOURCE_DIR,
    *,
    long_edge: int = 2000,
    jpeg_quality: int = 82,
) -> dict[str, Any]:
    resized = []
    for path in sorted(directory.glob("*")):
        if not path.is_file():
            continue
        try:
            with Image.open(path) as source:
                source.load()
                original_size = source.size
                if max(original_size) <= long_edge:
                    continue
                image = ImageOps.exif_transpose(source)
                scale = long_edge / max(image.size)
                target_size = (
                    max(1, round(image.width * scale)),
                    max(1, round(image.height * scale)),
                )
                image = image.resize(target_size, Image.Resampling.LANCZOS)
                before_bytes = path.stat().st_size
                suffix = path.suffix.lower()
                if suffix in {".jpg", ".jpeg"}:
                    if image.mode != "RGB":
                        image = image.convert("RGB")
                    image.save(
                        path,
                        "JPEG",
                        quality=jpeg_quality,
                        optimize=True,
                        progressive=True,
                    )
                elif suffix == ".png":
                    # These PPT embeds are screenshots and maps with large flat
                    # color regions. Palette encoding preserves text and alpha
                    # edges while avoiding a larger file after downsampling.
                    method = (
                        Image.Quantize.FASTOCTREE
                        if image.mode == "RGBA"
                        else Image.Quantize.MEDIANCUT
                    )
                    image = image.quantize(colors=256, method=method)
                    image.save(path, "PNG", optimize=True)
                else:
                    image.save(path)
                resized.append(
                    {
                        "path": path.relative_to(ROOT).as_posix(),
                        "before_size": list(original_size),
                        "after_size": list(target_size),
                        "before_bytes": before_bytes,
                        "after_bytes": path.stat().st_size,
                    }
                )
        except OSError:
            continue
    return {
        "long_edge": long_edge,
        "jpeg_quality": jpeg_quality,
        "resized_count": len(resized),
        "images": resized,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, default=SOURCE_DIR)
    parser.add_argument("--long-edge", type=int, default=2000)
    parser.add_argument("--jpeg-quality", type=int, default=82)
    args = parser.parse_args()
    result = resize_oversized_images(
        args.directory,
        long_edge=args.long_edge,
        jpeg_quality=args.jpeg_quality,
    )
    source_manifest = ROOT / "data" / "crane-ppt-insights" / "source.json"
    if source_manifest.exists():
        payload = json.loads(source_manifest.read_text(encoding="utf-8"))
        payload["resized_oversized_assets"] = result["resized_count"]
        payload["source_image_long_edge_limit"] = result["long_edge"]
        source_manifest.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
