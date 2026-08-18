"""Resolve the governed excavator market-insight source deck."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "data" / "source-presentations"
MANIFEST_PATH = SOURCE_DIR / "source-manifest.json"


def source_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        return {}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def source_pptx() -> Path:
    manifest = source_manifest()
    filename = manifest.get("current_excavator_market_deck", {}).get("filename")
    if filename:
        path = SOURCE_DIR / filename
        if path.exists():
            return path
    files = sorted(
        SOURCE_DIR.glob("*.pptx"), key=lambda item: item.stat().st_mtime, reverse=True
    )
    if not files:
        raise FileNotFoundError(f"No presentation found in {SOURCE_DIR}")
    return files[0]


def validate_source() -> dict:
    path = source_pptx()
    digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
    expected = source_manifest().get("current_excavator_market_deck", {})
    expected_digest = str(expected.get("sha256") or "").upper()
    if expected_digest and digest != expected_digest:
        raise RuntimeError(
            f"Source presentation hash mismatch: {digest} != {expected_digest}"
        )
    return {"path": path, "sha256": digest, "size_bytes": path.stat().st_size}
