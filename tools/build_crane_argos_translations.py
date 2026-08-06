from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from argostranslate import translate

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "crane-ppt-insights" / "slides.json"
OUTPUT = ROOT / "data" / "crane-ppt-insights" / "translations.en.json"


GLOSSARY = {
    "越野轮胎起重机": "rough-terrain crane",
    "越野轮胎吊": "rough-terrain crane",
    "越野吊": "rough-terrain crane",
    "全地面起重机": "all-terrain crane",
    "全地面吊": "all-terrain crane",
    "履带起重机": "crawler crane",
    "履带吊": "crawler crane",
    "通用底盘起重机": "boom truck",
    "汽车起重机": "truck crane",
    "随车起重机": "boom truck",
    "折臂吊": "knuckle-boom crane",
    "伸缩臂叉装车": "telehandler",
    "高空作业平台": "aerial work platform",
    "行走减速机": "travel reduction gearbox",
    "主卷扬": "main winch",
    "副卷扬": "auxiliary winch",
    "卷扬": "winch",
    "主臂": "main boom",
    "基本臂": "base boom",
    "副臂": "jib",
    "桁架臂": "lattice boom",
    "伸缩臂": "telescopic boom",
    "支腿跨距": "outrigger span",
    "支腿": "outrigger",
    "配重": "counterweight",
    "吊钩": "hook block",
    "钢丝绳": "wire rope",
    "单绳拉力": "single-line pull",
    "起升高度": "lifting height",
    "工作半径": "working radius",
    "额定起重量": "rated lifting capacity",
    "最大起重量": "maximum lifting capacity",
    "吊重": "lifting capacity",
    "吊装": "lifting operation",
    "载荷表": "load chart",
    "力矩限制器": "rated-capacity limiter",
    "力矩": "load moment",
    "回转速度": "swing speed",
    "回转": "swing",
    "变幅": "luffing",
    "伸缩": "telescoping",
    "微动性": "fine-control performance",
    "操控性": "controllability",
    "舒适性": "operator comfort",
    "维修性": "serviceability",
    "可靠性": "reliability",
    "安全性": "safety",
    "经济性": "economy",
    "性价比": "value for money",
    "人性化配置": "operator-ergonomics equipment",
    "人性化": "operator ergonomics",
    "软文资料": "sales literature",
    "工况适应性": "work-condition adaptability",
    "可售型谱": "saleable product portfolio",
    "型谱覆盖率": "portfolio coverage",
    "型谱": "product portfolio",
    "转场能力": "jobsite-travel capability",
    "转场": "jobsite travel",
    "支车": "setting the outriggers",
    "收车": "retracting the outriggers",
    "整机运输重量": "machine transport weight",
    "整机": "machine",
    "竞品": "competitor",
    "标杆竞品": "benchmark competitor",
    "标杆": "benchmark",
    "样机": "prototype",
    "通过性": "off-road mobility",
    "上车": "upperstructure",
    "下车": "carrier",
    "驾驶室": "operator cab",
    "发动机": "engine",
    "液压系统": "hydraulic system",
    "传动系统": "drivetrain",
    "北美": "North America",
    "美国": "United States",
    "加拿大": "Canada",
    "徐工": "XCMG",
    "卡特彼勒": "Caterpillar",
    "卡特": "Caterpillar",
    "小松": "Komatsu",
    "久保田": "Kubota",
    "约翰迪尔": "John Deere",
    "迪尔": "John Deere",
    "三一": "SANY",
    "柳工": "LiuGong",
    "山猫": "Bobcat",
    "多田野": "Tadano",
    "利勃海尔": "Liebherr",
    "格鲁夫": "Grove",
    "特雷克斯": "Terex",
    "马尼托瓦克": "Manitowoc",
}

CORRECTIONS = {
    "cross-country tyre crane": "rough-terrain crane",
    "cross-country tire crane": "rough-terrain crane",
    "rough terrain crane": "rough-terrain crane",
    "all terrain crane": "all-terrain crane",
    "Xugong": "XCMG",
    "Xuzhou Heavy Industries": "XCMG",
    "John Dill": "John Deere",
    "John Deere Deere": "John Deere",
    "Cater": "Caterpillar",
    "Boom trick": "boom truck",
    "Boomtt": "boom truck",
    "Boom truck": "boom truck",
    "general chassis crane": "boom truck",
    "generic chassis crane": "boom truck",
    "universal chassis crane": "boom truck",
    "generic chassis": "boom-truck chassis",
    "universal chassis": "boom-truck chassis",
    "full-truck capacity": "all-terrain crane",
    "full-truck crane": "all-terrain crane",
    "full-truck": "all-terrain crane",
    "ground-wide crane": "all-terrain crane",
    "ground-wide": "all-terrain crane",
    "RV crane": "rough-terrain crane",
    "R.V. crane": "rough-terrain crane",
    "Cross-country tyres": "Rough-terrain cranes",
    "cross-country tyres": "rough-terrain cranes",
    "unrigger": "outrigger",
    "Reducation": "Reduction",
    "reducation": "reduction",
    "main arm": "main boom",
    "basic arm": "base boom",
    "secondary arm": "jib",
    "support leg": "outrigger",
    "walking reducer": "travel reduction gearbox",
    "complete vehicle": "machine",
    "whole vehicle": "machine",
    "whole machine": "machine",
    "humanization": "operator ergonomics",
    "Humanization": "Operator ergonomics",
    "humanized": "ergonomic",
    "Humanized": "Ergonomic",
    "relibrity": "reliability",
    "relibility": "reliability",
    "telecoping": "telescoping",
    "wirre rope": "wire rope",
    "industry poles": "industry benchmark",
    "value of sex": "value for money",
    "pinion": "pin",
}


def protect_terms(text: str) -> str:
    for source, target in sorted(GLOSSARY.items(), key=lambda item: len(item[0]), reverse=True):
        text = text.replace(source, target)
    return text


def clean_translation(text: str) -> str:
    for source, target in CORRECTIONS.items():
        text = text.replace(source, target)
    text = re.sub(r"\s+([,.;:%)])", r"\1", text)
    text = re.sub(r"([(])\s+", r"\1", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text


def batches(values: list[str], max_items: int = 80, max_chars: int = 7000):
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


def translate_group(values: list[str]) -> list[str]:
    source = "\n".join(f"[{index}]\n{protect_terms(value)}" for index, value in enumerate(values))
    translated = translate.translate(source, "zh", "en")
    matches = list(re.finditer(r"(?m)^\[(\d+)\]\s*$", translated))
    by_index: dict[int, str] = {}
    for position, match in enumerate(matches):
        index = int(match.group(1))
        start = match.end()
        end = matches[position + 1].start() if position + 1 < len(matches) else len(translated)
        by_index[index] = clean_translation(translated[start:end].strip())
    if len(by_index) == len(values) and all(by_index.get(index) for index in range(len(values))):
        return [by_index[index] for index in range(len(values))]
    if len(values) == 1:
        return [clean_translation(translate.translate(protect_terms(values[0]), "zh", "en"))]
    midpoint = len(values) // 2
    return translate_group(values[:midpoint]) + translate_group(values[midpoint:])


def main() -> None:
    arguments = [value for value in sys.argv[1:] if not value.startswith("--")]
    if not arguments:
        raise SystemExit("Pass the JSON file exported by collect_strings as the first argument")
    source_strings = json.loads(Path(arguments[0]).read_text(encoding="utf-8"))
    payload = json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else {}
    cache = {} if "--force" in sys.argv else (payload.get("translations") or {})
    pending = [source for source in source_strings if not cache.get(source)]
    groups = list(batches(pending))
    completed = 0
    for group_index, group in enumerate(groups, 1):
        cache.update(zip(group, translate_group(group)))
        completed += len(group)
        OUTPUT.write_text(
            json.dumps(
                {
                    "model": "argos-translate-zh-en-1.9 with XCMG crane terminology",
                    "translation_scope": "crane PPT reader-facing text; generated fully offline",
                    "source_count": len(source_strings),
                    "translations": dict(sorted(cache.items())),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print(
            f"Translated batch {group_index}/{len(groups)} ({completed}/{len(pending)}); "
            f"cache {len(cache)}/{len(source_strings)}",
            flush=True,
        )


if __name__ == "__main__":
    main()
