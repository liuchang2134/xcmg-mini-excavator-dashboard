import collections
import hashlib
import json
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGES = [
    "crane-rt-60t",
    "crane-rt-75t",
    "crane-rt-100t",
    "crane-rt-130t",
    "crane-rt-160t",
    "crane-at-150t",
    "crane-market-overview",
]


def main() -> None:
    captions: dict[str, set[tuple[str, str]]] = collections.defaultdict(set)
    paths: dict[str, list[str]] = collections.defaultdict(list)
    image_pattern = re.compile(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"')

    for page in PAGES:
        html_path = ROOT / f"{page}.html"
        if not html_path.exists():
            continue
        html = html_path.read_text(encoding="utf-8", errors="ignore")
        for match in image_pattern.finditer(html):
            source, caption = match.groups()
            image_path = ROOT / source
            if not image_path.exists():
                continue
            digest = hashlib.md5(image_path.read_bytes()).hexdigest()
            captions[digest].add((page, caption))
            paths[digest].append(source)

    conflicts = [
        {
            "hash": digest,
            "files": sorted(set(paths[digest])),
            "usages": [
                {"page": page, "caption": caption}
                for page, caption in sorted(usages)
            ],
        }
        for digest, usages in captions.items()
        if len({caption for _, caption in usages}) > 1
    ]
    output_path = ROOT / "crane-image-conflicts.json"
    output_path.write_text(
        json.dumps(conflicts, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"冲突 {len(conflicts)} 组")


if __name__ == "__main__":
    main()
