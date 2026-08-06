from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "crane-ppt-insights" / "slides.json"
OUTPUT = ROOT / "data" / "crane-ppt-insights" / "translations.en.json"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen3:1.7b"
FALLBACK_MODEL = "qwen3:8b"
HAN = re.compile(r"[\u3400-\u9fff]")
MANUAL_TRANSLATIONS = {
    "16万N.m行走减速机": "160,000 N.m travel reduction gearbox",
}

SYSTEM_PROMPT = """You are a senior North American crane product engineer and technical editor.
Translate every Chinese source string into clear, professional US English for an internal XCMG ARC competitive-benchmarking website.

Rules:
- Translate completely. Do not summarize, omit, add, or reinterpret facts.
- Preserve all numbers, dates, percentages, units, model codes, list numbering, line breaks, and uncertainty/status language.
- Use established crane terminology: rough-terrain crane, all-terrain crane, boom truck, crawler crane, main boom, jib, counterweight, outrigger, load chart, pick-and-carry, winch, line pull, telematics, serviceability.
- Brand glossary: 徐工=XCMG, 卡特=Caterpillar, 小松=Komatsu, 久保田=Kubota, 约翰迪尔=John Deere, 三一=SANY, 柳工=LiuGong, 山猫=Bobcat, 多田野=Tadano, 利勃海尔=Liebherr, 格鲁夫=Grove, 特雷克斯=Terex, 马尼托瓦克=Manitowoc.
- Use US English grammar and natural business/engineering syntax.
- Return JSON only, following the requested schema. Never include markdown.
"""


def collect_strings(slides: list[dict[str, Any]]) -> list[str]:
    values: set[str] = set()
    try:
        from tools.crane_ppt_render import (
            IMAGE_CAPTION_OVERRIDES,
            SECTION_LABELS,
            _display_title,
        )
    except ImportError:
        from crane_ppt_render import (
            IMAGE_CAPTION_OVERRIDES,
            SECTION_LABELS,
            _display_title,
        )

    values.update(SECTION_LABELS.values())
    values.update(
        caption
        for captions in IMAGE_CAPTION_OVERRIDES.values()
        for caption in captions
    )
    for slide in slides:
        values.add(str(slide.get("title") or "").strip())
        values.add(_display_title(slide))
        for block in slide.get("text_blocks", []):
            text = str(block.get("text") or "").strip()
            values.add(text)
            values.update(part.strip() for part in re.split(r"\n(?=\S)", text))
        for table in slide.get("tables", []):
            for row in table.get("rows", []):
                values.update(str(cell).strip() for cell in row)
        for chart in slide.get("charts", []):
            values.update(str(item).strip() for item in chart.get("categories", []))
            values.update(
                str(series.get("name") or "").strip()
                for series in chart.get("series", [])
            )
    return sorted(value for value in values if value and HAN.search(value))


def batches(values: list[str], max_items: int = 60, max_chars: int = 2500):
    current: list[str] = []
    size = 0
    for value in values:
        if current and (len(current) >= max_items or size + len(value) > max_chars):
            yield current
            current = []
            size = 0
        current.append(value)
        size += len(value)
    if current:
        yield current


def request_translation(values: list[str], model: str = MODEL) -> list[str]:
    payload = {
        "model": model,
        "stream": False,
        "think": False,
        "format": {
            "type": "object",
            "properties": {
                "translations": {
                    "type": "array",
                    "items": {"type": "string"},
                }
            },
            "required": ["translations"],
        },
        "options": {"temperature": 0.05, "num_ctx": 8192},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Translate the following JSON array. Return an object with a translations array "
                    "of exactly the same length and order.\n" + json.dumps(values, ensure_ascii=False)
                ),
            },
        ],
    }
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=600) as response:
        result = json.loads(response.read().decode("utf-8"))
    content = json.loads(result["message"]["content"])
    translations = content.get("translations") or []
    if len(translations) != len(values):
        raise ValueError(f"Expected {len(values)} translations, received {len(translations)}")
    return [str(item).strip() for item in translations]


def translate_batch(values: list[str]) -> list[str]:
    for attempt in range(3):
        try:
            translated = request_translation(values)
            repaired = []
            for source, target in zip(values, translated):
                if source in MANUAL_TRANSLATIONS:
                    target = MANUAL_TRANSLATIONS[source]
                elif not target or HAN.search(target):
                    target = request_translation([source], FALLBACK_MODEL)[0]
                if not target or HAN.search(target):
                    raise ValueError(f"Residual Chinese in translation: {source[:80]}")
                repaired.append(target)
            return repaired
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError, json.JSONDecodeError):
            pass
        time.sleep(1 + attempt)
    if len(values) == 1:
        translated = request_translation(values, FALLBACK_MODEL)
        if translated[0] and not HAN.search(translated[0]):
            return translated
        raise RuntimeError(f"Could not translate source text: {values[0][:120]}")
    midpoint = len(values) // 2
    return translate_batch(values[:midpoint]) + translate_batch(values[midpoint:])


def main() -> None:
    slides = json.loads(SOURCE.read_text(encoding="utf-8"))
    source_strings = collect_strings(slides)
    cache: dict[str, str] = {}
    if OUTPUT.exists():
        cache = json.loads(OUTPUT.read_text(encoding="utf-8")).get("translations", {})

    pending = [value for value in source_strings if not cache.get(value)]
    groups = list(batches(pending))
    for index, group in enumerate(groups, 1):
        translated = translate_batch(group)
        cache.update(zip(group, translated))
        OUTPUT.write_text(
            json.dumps(
                {
                    "model": MODEL,
                    "translation_scope": "crane PPT reader-facing text; generated locally with Ollama",
                    "source_count": len(source_strings),
                    "translations": dict(sorted(cache.items())),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print(
            f"Translated batch {index}/{len(groups)} ({len(cache)}/{len(source_strings)})",
            flush=True,
        )

    missing = [value for value in source_strings if not cache.get(value)]
    if missing:
        raise RuntimeError(f"Missing {len(missing)} translations")


if __name__ == "__main__":
    main()
