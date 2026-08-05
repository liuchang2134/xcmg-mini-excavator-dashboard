from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert PowerPoint-rendered crane images to web-ready WebP files."
    )
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--quality", type=int, default=92)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    converted = 0
    for source_path in sorted(args.input_dir.glob("*.png")):
        output_path = args.output_dir / f"{source_path.stem}.webp"
        with Image.open(source_path) as image:
            image.load()
            image.save(
                output_path,
                "WEBP",
                quality=args.quality,
                method=4,
                exact=True,
            )
        converted += 1

    if converted == 0:
        raise RuntimeError(f"No PNG files found in {args.input_dir}")

    # Display assets are generated. Remove obsolete PNG versions only after all
    # WebP files have been written successfully.
    for stale_path in args.output_dir.glob("*.png"):
        stale_path.unlink()

    print(f"Optimized {converted} images into {args.output_dir}")


if __name__ == "__main__":
    main()
