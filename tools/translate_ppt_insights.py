"""Build reviewed English sidecars for the extracted PowerPoint insight data.

The Chinese extraction files remain authoritative and untouched. This tool
translates only strings that contain Han characters, checkpoints locally, and
writes deterministic English sidecar files consumed by the dashboard builders.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "ppt-insights"
SOURCE_PATH = DATA_DIR / "ppt-source-content.json"
TABLE_PATH = DATA_DIR / "ppt-business-tables.json"
GLOSSARY_PATH = DATA_DIR / "translation-glossary.json"
OVERRIDES_PATH = DATA_DIR / "translation-overrides.json"
SOURCE_EN_PATH = DATA_DIR / "ppt-source-content-en.json"
TABLE_EN_PATH = DATA_DIR / "ppt-business-tables-en.json"
CACHE_PATH = DATA_DIR / ".ppt-translation-cache.json"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
HAN = re.compile(r"[\u3400-\u9fff]")
DEFAULT_CT2_MODEL_PATH = ROOT / ".translation-models" / "opus-mt-zh-en"
TERM_ALTERNATIVES = {
    "计划": ("planned", "plan", "scheduled", "program", "initiative"),
    "预测": ("forecast", "projection", "projected"),
    "预计": ("estimate", "estimated", "expected", "projected"),
    "整机重量": ("operating weight", "operating mass", "machine weight"),
    "运输重量": ("transport weight", "shipping weight"),
    "标配": ("standard equipment", "standard", "standard-fit"),
    "选配": (
        "optional equipment",
        "optional",
        "available with",
        "available as an option",
        "offered with",
    ),
    "无配置": ("not available", "unavailable", "not offered"),
    "起吊力": ("lift capacity", "lifting capacity"),
    "辅助液压": ("auxiliary hydraulics", "auxiliary hydraulic"),
    "仪表": ("monitor", "display", "instrument panel", "instrument"),
    "属具": ("attachment", "implement", "tool"),
    "机具": (
        "attachment",
        "implement",
        "tool",
        "machinery",
        "equipment compatibility",
    ),
    "复合动作": (
        "combined operation",
        "combined-function",
        "simultaneous operation",
    ),
    "动作协调性": ("coordination", "combined-function response"),
    "动作柔和性": ("control smoothness", "smooth response"),
    "微操控性": ("fine control", "precision control", "micro-control"),
    "平地": ("grading", "fine grading"),
    "动臂": ("boom",),
    "回转力矩": ("swing torque", "slewing torque"),
    "四向推土铲": ("4-way dozer blade", "four-way dozer blade"),
    "浮动功能": (
        "float function",
        "float mode",
        "blade float",
        "boom float",
        "float feature",
        "float capability",
    ),
    "推土铲偏摆": ("dozer blade angle", "angle blade", "blade angling"),
    "副配重": (
        "additional counterweight",
        "add-on counterweight",
        "auxiliary counterweight",
    ),
    "可拆卸配重": ("removable counterweight",),
    "伸缩式底盘": (
        "variable-width undercarriage",
        "retractable undercarriage",
        "expandable undercarriage",
    ),
    "支重轮": ("track roller", "lower roller"),
    "卸油管路": ("case drain line", "drain line"),
    "机具合流": ("combined-flow circuit", "combined hydraulic flow"),
    "PTO泵": ("pto pump",),
    "液控负载敏感系统": (
        "pilot-operated load-sensing hydraulic system",
        "pilot-operated load-sensing system",
    ),
    "电控正流量系统": (
        "electronically controlled positive-flow hydraulic system",
        "electronic positive-flow control",
    ),
    "手机支架": ("phone holder", "phone mount"),
    "行走蜂鸣器": ("travel alarm", "travel buzzer"),
    "消音功能": ("alarm mute function", "mute function"),
    "手柄": (
        "joystick",
        "control lever",
        "control handle",
        "blade control",
        "blade lever",
        "blade handle",
        "dozer blade handle",
        "lever",
    ),
    "橡胶履带板": ("rubber track pads", "rubber tracks"),
}


def normalize_translation(source, value):
    value = re.sub(r"[ \t]+", " ", str(value or ""))
    value = re.sub(r" *\n *", "\n", value)
    value = re.sub(r"\s+([,.;:!?%])", r"\1", value)
    replacements = {
        r"\bexcavers?\b": "excavators",
        r"\btonsnage\b": "tonnage",
        r"\bequipement\b": "equipment",
        r"\bflatits\b": "platforms",
        r"\barmcontrollability\b": "arm controllability",
        r"\bandforecast\b": "and forecast",
        r"\bXCMG(?=XE\d)": "XCMG ",
        r"\bground level(?=\d)": "ground level ",
        r"(?<=\d)m(?=lift capacity)": " m ",
    }
    for pattern, replacement in replacements.items():
        value = re.sub(pattern, replacement, value, flags=re.I)
    if "机型" in source:
        value = re.sub(r"\baircraft\b", "model", value, flags=re.I)
    if "手机支架" in source:
        value = re.sub(
            r"\b(?:cellular|mobile phone|cell phone) "
            r"(?:support|rack|staircase|holder|mount)s?\b",
            "phone holder",
            value,
            flags=re.I,
        )
    if "仪表" in source:
        value = re.sub(
            r"\b(?:metric|meter|instrument)(?=\s|$)",
            "monitor",
            value,
            flags=re.I,
        )
    if "消音功能" in source:
        value = re.sub(
            r"\b(?:noise reduction function|(?:alarm\s+)?"
            r"(?:silencer|silencing|muting|mute)"
            r"(?:\s+function)?)\b",
            "alarm mute function",
            value,
            flags=re.I,
        )
    if "微操控性" in source:
        value = re.sub(
            r"\bmicro[- ]?controll?ability\b",
            "fine control",
            value,
            flags=re.I,
        )
    if "复合动作" in source:
        value = re.sub(
            r"\b(?:composite|complex)\s+(?:action|operation)s?\b",
            "combined operation",
            value,
            flags=re.I,
        )
    if "属具" in source or "机具" in source:
        value = re.sub(
            r"\bmachine tools?\b|\bfacilities\b|\bmachinery\b",
            "attachments",
            value,
            flags=re.I,
        )
        value = re.sub(
            r"\bequipment compatibility\b",
            "attachment compatibility",
            value,
            flags=re.I,
        )
    if "副配重" in source:
        value = re.sub(
            r"\b(?:auxiliary counterweight|sub-heavy|by[- ]product|by weights?)\b",
            "additional counterweight",
            value,
            flags=re.I,
        )
    if "橡胶履带板" in source:
        value = re.sub(
            r"\brubber track (?:block|board)s?\b",
            "rubber track pads",
            value,
            flags=re.I,
        )
    if "卸油管路" in source:
        value = re.sub(
            r"\b(?:fuel line|offline|drainage pipeline)\b",
            "case drain line",
            value,
            flags=re.I,
        )
    if "可拆卸配重" in source:
        value = re.sub(
            r"\bundismantled\b",
            "removable counterweight",
            value,
            flags=re.I,
        )
    if "伸缩式底盘" in source:
        value = re.sub(
            r"\b(?:non-?)?scalable chassis\b",
            "variable-width undercarriage",
            value,
            flags=re.I,
        )
    if "影响装车效率" in source:
        value = re.sub(
            r"\bvideo[- ]loading efficiency\b",
            "loading efficiency",
            value,
            flags=re.I,
        )
    value = re.sub(
        r"\bliquid control load sensitive system\b",
        "pilot-operated load-sensing system",
        value,
        flags=re.I,
    )
    return value.strip()


@dataclass(frozen=True)
class TranslationUnit:
    digest: str
    text: str


class OpusTranslator:
    """Fast local Chinese-to-English baseline using a CTranslate2 OPUS model."""

    def __init__(self, model_path, glossary):
        try:
            import ctranslate2
            import sentencepiece as spm
        except ImportError as error:
            raise RuntimeError(
                "CTranslate2 backend requires ctranslate2 and sentencepiece. "
                "Use the repository translation virtual environment."
            ) from error

        model_path = Path(model_path)
        if not (model_path / "model.bin").exists():
            raise FileNotFoundError(f"Translation model not found: {model_path}")
        self.source_processor = spm.SentencePieceProcessor(
            model_file=str(model_path / "source.spm")
        )
        self.target_processor = spm.SentencePieceProcessor(
            model_file=str(model_path / "target.spm")
        )
        self.translator = ctranslate2.Translator(
            str(model_path),
            device="cpu",
            compute_type="int8",
            inter_threads=2,
            intra_threads=8,
        )
        self.glossary_terms = sorted(
            glossary.get("terms", {}).items(),
            key=lambda item: len(item[0]),
            reverse=True,
        )

    def prepare_source(self, value):
        prepared = str(value or "")
        for chinese, english in self.glossary_terms:
            if chinese in prepared:
                prepared = prepared.replace(chinese, english)
        return prepared

    @staticmethod
    def split_segments(value, max_chars=320):
        segments = []
        lines = str(value or "").splitlines() or [str(value or "")]
        for line_index, line in enumerate(lines):
            line = line.strip()
            if not line:
                if segments:
                    text, _separator = segments[-1]
                    segments[-1] = (text, "\n")
                continue
            sentences = [
                item.strip()
                for item in re.split(r"(?<=[。！？；;!?])", line)
                if item.strip()
            ]
            if not sentences:
                sentences = [line]
            expanded = []
            for sentence in sentences:
                if len(sentence) <= max_chars:
                    expanded.append(sentence)
                    continue
                clauses = [
                    item.strip()
                    for item in re.split(r"(?<=[，,、：:])", sentence)
                    if item.strip()
                ]
                buffer = ""
                for clause in clauses:
                    if buffer and len(buffer) + len(clause) > max_chars:
                        expanded.append(buffer)
                        buffer = clause
                    else:
                        buffer += clause
                if buffer:
                    expanded.append(buffer)
            for index, sentence in enumerate(expanded):
                is_last = index == len(expanded) - 1
                separator = "\n" if is_last and line_index < len(lines) - 1 else " "
                segments.append((sentence, separator))
        return segments or [("", "")]

    @staticmethod
    def replace_case_insensitive(value, source, target):
        return re.sub(re.escape(source), lambda _match: target, value, flags=re.I)

    def repair_glossary_spelling(self, source, translation):
        output = translation
        word_pattern = re.compile(r"[A-Za-z][A-Za-z0-9.&+\-/]*")
        for chinese, expected in self.glossary_terms:
            if chinese not in source or expected.lower() in output.lower():
                continue
            target_words = word_pattern.findall(expected)
            output_words = list(word_pattern.finditer(output))
            if not target_words or not output_words:
                continue
            width = len(target_words)
            best = None
            expected_key = " ".join(target_words).lower()
            for start in range(len(output_words)):
                end = min(len(output_words), start + width)
                if end - start != width:
                    continue
                candidate = output[output_words[start].start() : output_words[end - 1].end()]
                ratio = difflib.SequenceMatcher(
                    None,
                    candidate.lower(),
                    expected_key,
                ).ratio()
                if best is None or ratio > best[0]:
                    best = (ratio, candidate)
            if best and best[0] >= 0.64:
                output = self.replace_case_insensitive(output, best[1], expected)
        return output

    @staticmethod
    def clean_translation(value):
        value = re.sub(
            r"\bengineering and machinery\b",
            "construction equipment",
            str(value or ""),
            flags=re.I,
        )
        return normalize_translation("", value)

    def translate(self, items):
        segment_map = []
        token_batches = []
        grouped = [[] for _item in items]
        for item_index, unit in enumerate(items):
            prepared = self.prepare_source(unit.text)
            for segment_index, (segment, separator) in enumerate(
                self.split_segments(prepared)
            ):
                if not HAN.search(segment):
                    grouped[item_index].append(
                        (segment_index, segment.strip() + separator)
                    )
                    continue
                tokens = self.source_processor.encode(segment, out_type=str)
                # Marian tokenizers append EOS. The converted model does not do
                # that automatically; omitting it causes repetition and truncation.
                token_batches.append(tokens + ["</s>"])
                segment_map.append((item_index, segment_index, separator))

        if token_batches:
            results = self.translator.translate_batch(
                token_batches,
                beam_size=4,
                max_decoding_length=512,
                repetition_penalty=1.1,
                no_repeat_ngram_size=4,
            )
            translated_segments = [
                self.target_processor.decode(result.hypotheses[0])
                for result in results
            ]
            for (item_index, segment_index, separator), translated_segment in zip(
                segment_map, translated_segments
            ):
                grouped[item_index].append(
                    (segment_index, translated_segment.strip() + separator)
                )

        output = []
        for unit, fragments in zip(items, grouped):
            translated_value = self.clean_translation(
                "".join(
                    fragment
                    for _index, fragment in sorted(
                        fragments, key=lambda item: item[0]
                    )
                )
            )
            translated_value = self.repair_glossary_spelling(
                unit.text, translated_value
            )
            output.append((unit.digest, translated_value))
        return output


def sha256_text(value):
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()


def load_json(path, default=None):
    if not path.exists():
        return {} if default is None else default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def source_hashes():
    hashes = {
        "ppt_source_sha256": hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest(),
        "ppt_tables_sha256": hashlib.sha256(TABLE_PATH.read_bytes()).hexdigest(),
        "glossary_sha256": hashlib.sha256(GLOSSARY_PATH.read_bytes()).hexdigest(),
    }
    if OVERRIDES_PATH.exists():
        hashes["translation_overrides_sha256"] = hashlib.sha256(
            OVERRIDES_PATH.read_bytes()
        ).hexdigest()
    return hashes


def apply_reviewed_overrides(cache, overrides, glossary):
    """Apply deterministic human-reviewed translations before model repair."""
    applied = 0
    for record in overrides.get("translations", []):
        source = str(record.get("source") or "").strip()
        english = str(record.get("en") or "").strip()
        if not source or not english:
            continue
        unit = TranslationUnit(sha256_text(source), source)
        english = validate_translation(unit, english, glossary)
        cache[unit.digest] = {
            "source": source,
            "en": english,
            "review": "human-reviewed engineering override",
        }
        applied += 1
    return applied


def collect_strings(source, tables):
    strings = {}

    def add(value):
        value = str(value or "").strip()
        if value and HAN.search(value):
            digest = sha256_text(value)
            strings.setdefault(digest, value)

    for slide in source.get("slides", []):
        add(slide.get("title", {}).get("zh"))
        for item in slide.get("body", []):
            add(item.get("zh"))
        for item in slide.get("notes", []):
            add(item.get("zh"))
        for visual in slide.get("visuals", []):
            chart = visual.get("chart_data") or {}
            add(chart.get("title"))
            for value in chart.get("categories", []):
                add(value)
            for series in chart.get("series", []):
                add(series.get("name"))
            for value in chart.get("axis_titles", []):
                add(value)

    for record in tables.get("records", []):
        add(record.get("title"))
        for row in record.get("matrix_zh", []):
            for cell in row:
                add(cell)

    return [
        TranslationUnit(digest=digest, text=text)
        for digest, text in sorted(strings.items(), key=lambda item: item[1])
    ]


def collect_source_strings(source):
    strings = {}

    def add(value):
        text = str(value or "").strip()
        if text and HAN.search(text):
            strings.setdefault(sha256_text(text), text)

    for slide in source.get("slides", []):
        add(slide.get("title", {}).get("zh"))
        for item in slide.get("body", []):
            add(item.get("zh"))
        for item in slide.get("notes", []):
            add(item.get("zh"))
        for visual in slide.get("visuals", []):
            chart = visual.get("chart_data") or {}
            add(chart.get("title"))
            for value in chart.get("categories", []):
                add(value)
            for series in chart.get("series", []):
                add(series.get("name"))
            for value in chart.get("axis_titles", []):
                add(value)

    return [
        TranslationUnit(digest=digest, text=text)
        for digest, text in sorted(strings.items(), key=lambda item: item[1])
    ]


def glossary_prompt(glossary):
    terms = glossary.get("terms", {})
    return "\n".join(f"- {source}: {target}" for source, target in terms.items())


def system_prompt(glossary):
    return f"""You are a senior US construction-equipment technical translator.
Translate Chinese into concise, professional US English for an excavator
competitive-benchmarking platform.

Rules:
1. Preserve every number, year, model name, acronym, symbol, unit and list number.
2. Preserve line breaks and the distinction between actual, estimate, forecast,
   planned action, open issue and completed result.
3. Never update, correct, summarize, embellish or infer facts.
4. Translate plans as planned actions, never as completed actions.
5. Use natural engineering English, not word-for-word Chinese syntax.
6. Return JSON only in this exact shape:
   {{"translations":[{{"id":"0","en":"..."}}]}}
7. Return one result for every input id and do not include commentary.

Preferred terminology:
{glossary_prompt(glossary)}
"""


def required_terms(source, glossary):
    required = set(glossary.get("required_terms", []))
    candidates = []
    for chinese, english in glossary.get("terms", {}).items():
        if chinese not in required or chinese not in source:
            continue
        if any(chinese in selected for selected, _target in candidates):
            continue
        candidates = [
            item for item in candidates if item[0] not in chinese
        ]
        candidates.append((chinese, english))
    return candidates


def missing_required_terms(source, translation, glossary):
    lowered = translation.lower()
    missing = []
    for chinese, english in required_terms(source, glossary):
        alternatives = TERM_ALTERNATIVES.get(chinese)
        if alternatives:
            if not any(term in lowered for term in alternatives):
                missing.append(f"{chinese} ({'/'.join(alternatives)})")
            continue
        if english.lower() not in lowered:
            missing.append(english)
    return missing


def validate_translation(unit, value, glossary):
    value = normalize_translation(unit.text, value)
    if not value:
        raise ValueError("Translation is empty")
    if HAN.search(value):
        raise ValueError("Translation still contains Chinese")
    missing_terms = missing_required_terms(unit.text, value, glossary)
    if missing_terms:
        raise ValueError(
            "Translation is missing glossary terms: " + ", ".join(missing_terms)
        )
    return value


def decode_json_object(content):
    """Decode a model JSON object and close containers truncated after valid values."""
    start = content.find("{")
    if start < 0:
        raise ValueError("Ollama did not return a JSON object")
    candidate = content[start:]
    stack = []
    in_string = False
    escaped = False
    for index, character in enumerate(candidate):
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character in "[{":
            stack.append(character)
        elif character in "]}":
            expected = "[" if character == "]" else "{"
            if not stack or stack[-1] != expected:
                raise ValueError("Ollama returned structurally invalid JSON")
            stack.pop()
            if not stack:
                return json.loads(candidate[: index + 1])
    if in_string:
        raise ValueError("Ollama truncated JSON inside a string")
    repaired = candidate.rstrip() + "".join(
        "]" if opener == "[" else "}" for opener in reversed(stack)
    )
    return json.loads(repaired)


def ollama_chat(model, prompt, glossary, items, timeout):
    input_chars = sum(len(unit.text) for unit in items)
    body = {
        "model": model,
        "stream": False,
        "format": "json",
        "keep_alive": "30m",
        "options": {
            "temperature": 0,
            "num_ctx": 8192,
            # Chinese engineering prose expands substantially in English.
            # A generous output budget prevents truncated JSON and expensive retries.
            "num_predict": min(4096, max(512, int(input_chars * 2.0))),
        },
        "messages": [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": json.dumps(
                    [
                        {"id": str(index), "text": unit.text}
                        for index, unit in enumerate(items)
                    ],
                    ensure_ascii=False,
                ),
            },
        ],
    }
    if model.lower().startswith("qwen3"):
        body["think"] = False
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.load(response)
    content = payload.get("message", {}).get("content", "")
    decoded = decode_json_object(content)
    results = decoded.get("translations")
    if not isinstance(results, list):
        raise ValueError("Ollama response has no translations array")
    by_id = {str(item.get("id")): str(item.get("en") or "").strip() for item in results}
    translations = []
    for index, unit in enumerate(items):
        value = by_id.get(str(index), "")
        try:
            value = validate_translation(unit, value, glossary)
        except ValueError as error:
            raise ValueError(f"Translation for batch item {index}: {error}") from error
        translations.append((unit.digest, value))
    return translations


def ollama_translate_single(model, prompt, glossary, item, timeout):
    """Translate one stubborn item without relying on a JSON envelope."""
    body = {
        "model": model,
        "stream": False,
        "keep_alive": "30m",
        "options": {
            "temperature": 0,
            "num_ctx": 8192,
            "num_predict": min(2048, max(256, int(len(item.text) * 3.2))),
        },
        "messages": [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": (
                    "Translate the following single Chinese item into professional "
                    "North American construction-equipment English. Return only the "
                    "English translation, without JSON, labels, quotation marks, or "
                    f"commentary:\n\n{item.text}"
                ),
            },
        ],
    }
    if model.lower().startswith("qwen3"):
        body["think"] = False
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.load(response)
    value = str(payload.get("message", {}).get("content", "")).strip()
    value = re.sub(r"^```(?:text|english)?\s*|\s*```$", "", value, flags=re.I)
    value = re.sub(r"^(?:translation|english)\s*:\s*", "", value, flags=re.I)
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1].strip()
    value = validate_translation(item, value, glossary)
    return [(item.digest, value)]


def translate_batch(
    model,
    prompt,
    glossary,
    items,
    timeout,
    retries=3,
    secondary_model="",
    segment_retry=True,
):
    last_error = None
    for attempt in range(retries):
        try:
            return ollama_chat(model, prompt, glossary, items, timeout)
        except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
            last_error = error
            time.sleep(1.5 * (attempt + 1))
    if len(items) > 1:
        midpoint = max(1, len(items) // 2)
        return (
            translate_batch(
                model,
                prompt,
                glossary,
                items[:midpoint],
                timeout,
                retries,
                secondary_model,
                segment_retry,
            )
            + translate_batch(
                model,
                prompt,
                glossary,
                items[midpoint:],
                timeout,
                retries,
                secondary_model,
                segment_retry,
            )
        )
    for attempt in range(retries):
        try:
            return ollama_translate_single(
                model,
                prompt,
                glossary,
                items[0],
                timeout,
            )
        except (urllib.error.URLError, TimeoutError, ValueError) as error:
            last_error = error
            time.sleep(1.5 * (attempt + 1))
    if secondary_model and secondary_model != model:
        return translate_batch(
            secondary_model,
            prompt,
            glossary,
            items,
            timeout,
            retries=1,
            segment_retry=segment_retry,
        )
    if segment_retry:
        segments = OpusTranslator.split_segments(items[0].text, max_chars=72)
        if len(segments) > 1:
            translated_segments = []
            for segment, separator in segments:
                segment = segment.strip()
                if not segment:
                    translated_segments.append(separator)
                    continue
                segment_unit = TranslationUnit(sha256_text(segment), segment)
                result = translate_batch(
                    model,
                    prompt,
                    glossary,
                    [segment_unit],
                    timeout,
                    retries=1,
                    segment_retry=False,
                )
                translated_segments.append(dict(result)[segment_unit.digest] + separator)
            combined = normalize_translation(
                items[0].text,
                "".join(translated_segments),
            )
            return [
                (
                    items[0].digest,
                    validate_translation(items[0], combined, glossary),
                )
            ]
    raise RuntimeError(f"Could not translate {items[0].text!r}: {last_error}")


def make_batches(units, max_items, max_chars):
    batch = []
    char_count = 0
    for unit in units:
        unit_chars = len(unit.text)
        if batch and (len(batch) >= max_items or char_count + unit_chars > max_chars):
            yield batch
            batch = []
            char_count = 0
        batch.append(unit)
        char_count += unit_chars
    if batch:
        yield batch


def translated(value, cache):
    text = str(value or "")
    if not HAN.search(text):
        return text
    return normalize_translation(
        text,
        cache.get(sha256_text(text), {}).get("en", ""),
    )


def compile_source_sidecar(source, cache, model, backend):
    slides = {}
    for slide in source.get("slides", []):
        visual_records = []
        for visual in slide.get("visuals", []):
            chart = visual.get("chart_data") or {}
            if not chart:
                visual_records.append({})
                continue
            visual_records.append(
                {
                    "chart_data": {
                        "title": translated(chart.get("title"), cache),
                        "categories": [
                            translated(value, cache) for value in chart.get("categories", [])
                        ],
                        "series_names": [
                            translated(item.get("name"), cache)
                            for item in chart.get("series", [])
                        ],
                        "axis_titles": [
                            translated(value, cache)
                            for value in chart.get("axis_titles", [])
                        ],
                    }
                }
            )
        slides[slide["id"]] = {
            "title": translated(slide.get("title", {}).get("zh"), cache),
            "body": [
                translated(item.get("zh"), cache) for item in slide.get("body", [])
            ],
            "notes": [
                translated(item.get("zh"), cache) for item in slide.get("notes", [])
            ],
            "visuals": visual_records,
        }
    return {
        "meta": {
            **source_hashes(),
            "model": model,
            "backend": backend,
            "language": "en-US",
            "method": "Local translation with XCMG engineering glossary",
        },
        "slides": slides,
    }


def compile_table_sidecar(tables, cache, model, backend):
    records = {}
    for record in tables.get("records", []):
        records[record["id"]] = {
            "title": translated(record.get("title"), cache),
            "matrix": [
                [translated(cell, cache) for cell in row]
                for row in record.get("matrix_zh", [])
            ],
        }
    return {
        "meta": {
            **source_hashes(),
            "model": model,
            "backend": backend,
            "language": "en-US",
            "method": "Local translation with XCMG engineering glossary",
        },
        "records": records,
    }


def translation_quality(units, cache, glossary):
    missing = []
    chinese = []
    glossary_issues = []
    for unit in units:
        item = cache.get(unit.digest, {})
        value = str(item.get("en") or "").strip()
        if not value:
            missing.append(unit.text)
        elif HAN.search(value):
            chinese.append((unit.text, value))
        else:
            missing_terms = missing_required_terms(unit.text, value, glossary)
            if missing_terms:
                glossary_issues.append((unit.text, value, missing_terms))
    return missing, chinese, glossary_issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=("ct2", "ollama"), default="ct2")
    parser.add_argument("--model", default="qwen3:4b")
    parser.add_argument("--ct2-model", default=str(DEFAULT_CT2_MODEL_PATH))
    parser.add_argument("--fallback-model", default="")
    parser.add_argument("--secondary-fallback-model", default="")
    parser.add_argument("--max-items", type=int, default=24)
    parser.add_argument("--max-chars", type=int, default=2600)
    parser.add_argument("--timeout", type=int, default=360)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--reset", action="store_true")
    parser.add_argument(
        "--review-source",
        action="store_true",
        help=(
            "Retranslate all slide titles, narrative, notes and chart labels with "
            "the selected Ollama model while retaining table-cell translations."
        ),
    )
    parser.add_argument(
        "--repair-invalid",
        action="store_true",
        help=(
            "Retranslate cached items that fail the current glossary or language "
            "validation rules."
        ),
    )
    args = parser.parse_args()
    if args.review_source and args.repair_invalid:
        parser.error("--review-source and --repair-invalid are mutually exclusive")
    if (args.review_source or args.repair_invalid) and args.backend != "ollama":
        parser.error("--review-source and --repair-invalid require --backend ollama")

    source = load_json(SOURCE_PATH)
    tables = load_json(TABLE_PATH)
    glossary = load_json(GLOSSARY_PATH)
    overrides = load_json(OVERRIDES_PATH, {"translations": []})
    units = collect_strings(source, tables)
    cache_payload = {} if args.reset else load_json(CACHE_PATH, {"translations": {}})
    cache = cache_payload.setdefault("translations", {})
    override_count = apply_reviewed_overrides(cache, overrides, glossary)
    all_pending = [unit for unit in units if not cache.get(unit.digest, {}).get("en")]
    if args.review_source:
        pending = collect_source_strings(source)
    elif args.repair_invalid:
        pending = []
        for unit in units:
            try:
                validate_translation(
                    unit,
                    cache.get(unit.digest, {}).get("en", ""),
                    glossary,
                )
            except ValueError:
                pending.append(unit)
    else:
        pending = all_pending
    if args.limit:
        pending = pending[: args.limit]
    prompt = system_prompt(glossary)
    batches = list(make_batches(pending, args.max_items, args.max_chars))
    ct2_translator = (
        OpusTranslator(args.ct2_model, glossary)
        if args.backend == "ct2"
        else None
    )
    model_label = (
        f"ct2:{Path(args.ct2_model).name}"
        if args.backend == "ct2"
        else args.model
    )
    if args.review_source:
        previous_model = str(cache_payload.get("meta", {}).get("model") or "").strip()
        model_label = (
            f"{previous_model} + {args.model} source review"
            if previous_model
            else f"{args.model} source review"
        )
    elif args.repair_invalid:
        previous_model = str(cache_payload.get("meta", {}).get("model") or "").strip()
        model_label = (
            f"{previous_model} + {args.model} glossary repair"
            if previous_model
            else f"{args.model} glossary repair"
        )

    print(
        f"Translation units: {len(units):,}; cached: {len(units) - len(all_pending):,}; "
        f"{'source review' if args.review_source else 'invalid review' if args.repair_invalid else 'pending this run'}: "
        f"{len(pending):,}; batches: {len(batches):,}; reviewed overrides: "
        f"{override_count:,}"
    )
    for batch_index, batch in enumerate(batches, start=1):
        if ct2_translator:
            results = ct2_translator.translate(batch)
            result_by_digest = dict(results)
            invalid = []
            for unit in batch:
                try:
                    validate_translation(
                        unit,
                        result_by_digest.get(unit.digest, ""),
                        glossary,
                    )
                except ValueError:
                    invalid.append(unit)
            if invalid and args.fallback_model:
                repaired = translate_batch(
                    args.fallback_model,
                    prompt,
                    glossary,
                    invalid,
                    args.timeout,
                    retries=1,
                    secondary_model=args.secondary_fallback_model,
                )
                result_by_digest.update(repaired)
                results = list(result_by_digest.items())
        else:
            results = translate_batch(
                args.model,
                prompt,
                glossary,
                batch,
                args.timeout,
                retries=1,
                secondary_model=args.secondary_fallback_model,
            )
        for digest, value in results:
            source_text = next(unit.text for unit in batch if unit.digest == digest)
            cache[digest] = {"source": source_text, "en": value}
        cache_payload["meta"] = {
            **source_hashes(),
            "model": model_label,
            "backend": args.backend,
            "language": "en-US",
        }
        write_json(CACHE_PATH, cache_payload)
        print(
            f"[{batch_index:>3}/{len(batches)}] translated {len(batch):>2} items; "
            f"cache={len(cache):,}",
            flush=True,
        )

    missing, chinese, glossary_issues = translation_quality(units, cache, glossary)
    write_json(
        SOURCE_EN_PATH,
        compile_source_sidecar(source, cache, model_label, args.backend),
    )
    write_json(
        TABLE_EN_PATH,
        compile_table_sidecar(tables, cache, model_label, args.backend),
    )
    print(
        json.dumps(
            {
                "units": len(units),
                "translated": len(units) - len(missing),
                "missing": len(missing),
                "chinese_in_english": len(chinese),
                "glossary_issues": len(glossary_issues),
                "source_sidecar": str(SOURCE_EN_PATH.relative_to(ROOT)),
                "table_sidecar": str(TABLE_EN_PATH.relative_to(ROOT)),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if not args.limit and (missing or chinese or glossary_issues):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
