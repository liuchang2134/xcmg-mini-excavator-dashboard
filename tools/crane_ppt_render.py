from __future__ import annotations

import html
import json
import math
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from PIL import Image

try:
    from .crane_ppt_insights import (
        CLASS_SECTION_SLIDES,
        CLASS_SLIDES,
        OUTPUT_DIR,
        SOURCE_DATE,
    )
    from .postedit_crane_translations import (
        MANUAL_OVERRIDES,
        deterministic_cleanup,
        generated_manual_override,
    )
except ImportError:
    from crane_ppt_insights import (
        CLASS_SECTION_SLIDES,
        CLASS_SLIDES,
        OUTPUT_DIR,
        SOURCE_DATE,
    )
    from postedit_crane_translations import (
        MANUAL_OVERRIDES,
        deterministic_cleanup,
        generated_manual_override,
    )


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DISPLAY_MANIFEST = ROOT / "data" / "crane-ppt-insights" / "image-display.json"
IMAGE_OWNERSHIP_MANIFEST = ROOT / "data" / "crane-ppt-insights" / "image-ownership.json"
TRANSLATION_FILE = ROOT / "data" / "crane-ppt-insights" / "translations.en.json"
THUMBNAIL_MANIFEST = ROOT / "data" / "crane-ppt-insights" / "image-thumbnails.json"


def _load_image_display_map() -> dict[str, str]:
    if not IMAGE_DISPLAY_MANIFEST.exists():
        return {}
    payload = json.loads(IMAGE_DISPLAY_MANIFEST.read_text(encoding="utf-8"))
    return {
        str(source): str(display)
        for source, display in (payload.get("images") or {}).items()
        if source and display
    }


IMAGE_DISPLAY_MAP = _load_image_display_map()


def _load_image_ownership_map() -> dict[str, dict[str, Any]]:
    if not IMAGE_OWNERSHIP_MANIFEST.exists():
        return {}
    payload = json.loads(IMAGE_OWNERSHIP_MANIFEST.read_text(encoding="utf-8"))
    return {
        str(source): dict(metadata)
        for source, metadata in (payload.get("assets") or {}).items()
        if source and isinstance(metadata, dict)
    }


IMAGE_OWNERSHIP_MAP = _load_image_ownership_map()


def _load_thumbnail_map() -> dict[str, str]:
    if not THUMBNAIL_MANIFEST.exists():
        return {}
    payload = json.loads(THUMBNAIL_MANIFEST.read_text(encoding="utf-8"))
    return {
        str(source): str(thumbnail)
        for source, thumbnail in (payload.get("images") or {}).items()
        if source and thumbnail
    }


THUMBNAIL_MAP = _load_thumbnail_map()


@lru_cache(maxsize=None)
def _source_image_size(path: str) -> tuple[int, int]:
    try:
        with Image.open(ROOT / path) as image:
            return image.size
    except (OSError, ValueError):
        return (0, 0)


@lru_cache(maxsize=None)
def _display_image_size(path: str) -> tuple[int, int]:
    """Return the rendered PowerPoint shape size, including picture cropping."""
    display_path = IMAGE_DISPLAY_MAP.get(path, path)
    try:
        with Image.open(ROOT / display_path) as image:
            return image.size
    except (OSError, ValueError):
        return _source_image_size(path)


def _preferred_image_asset(path: str) -> tuple[str, tuple[int, int], str]:
    """Use the complete source when the PowerPoint export is heavily cropped."""
    display_path = IMAGE_DISPLAY_MAP.get(path, path)
    source_size = _source_image_size(path)
    display_size = _display_image_size(path)
    source_width, source_height = source_size
    display_width, display_height = display_size
    if source_width and source_height and display_width and display_height:
        source_ratio = source_width / source_height
        display_ratio = display_width / display_height
        ratio_delta = abs(math.log(display_ratio / source_ratio))
        if ratio_delta > math.log(1.25):
            return path, source_size, "complete-source"
    return display_path, display_size, "ppt-export"


def _source_quality_class(path: str) -> str:
    long_edge = max(_source_image_size(path))
    if long_edge >= 1200:
        return "source-high"
    if long_edge >= 600:
        return "source-medium"
    return "source-low"


def _evidence_display_width(path: str) -> int:
    """Cap display width so small PPT embeds are not enlarged into blurry panels."""
    source_width, source_height = _source_image_size(path)
    _, (display_width, display_height), _ = _preferred_image_asset(path)
    long_edge = max(source_width, source_height)
    ratio = display_width / display_height if display_height else 1.0
    if long_edge <= 0:
        return 420
    if long_edge < 600:
        return min(420, max(180, round(source_width * 1.18)))
    if long_edge < 1200:
        return min(720, max(360, round(display_width * 0.72)))
    if ratio < 0.82:
        return min(420, max(300, round(display_width * 0.32)))
    if ratio > 3.2:
        return 1180
    return min(1040, max(520, display_width))


def _image_layout_class(path: str) -> str:
    _, (width, height), _ = _preferred_image_asset(path)
    ratio = width / height if height else 1.0
    if ratio >= 3.2:
        return "layout-panoramic"
    if ratio >= 1.45:
        return "layout-landscape"
    if ratio <= 0.82:
        return "layout-portrait"
    return "layout-standard"


def _image_aspect_group(path: str) -> str:
    width, height = _source_image_size(path)
    ratio = width / height if height else 1.0
    if ratio < 0.9:
        return "portrait"
    if ratio <= 1.15:
        return "square"
    return "landscape"


def _load_translations() -> dict[str, str]:
    if not TRANSLATION_FILE.exists():
        return {}
    payload = json.loads(TRANSLATION_FILE.read_text(encoding="utf-8"))
    return {
        str(source).strip(): str(target).strip()
        for source, target in (payload.get("translations") or {}).items()
        if source and target
    }


EN_TRANSLATIONS = _load_translations()


CRANE_ENGLISH_OVERRIDES = {
    "汽车起重机": "Truck-mounted crane",
    "占有率": "Market share",
    "占有率/%": "Market share (%)",
    "补充信息": "Additional information",
    "是否通用场景": "Common across regions",
    "竞品及型号": "Competitors and models",
    "客户群": "Customer segment",
    "客户对于关键参配的喜好": "Customer preferences for key specifications and equipment",
    "用户口碑": "Customer feedback",
    "徐工口碑": "XCMG customer feedback",
    "结论": "Conclusion",
    "销售价格/万美元": "Sales price (US$10,000)",
    "2.2 占有率分析及竞争对手锁定": "2.2 Market Share Analysis and Competitor Selection",
    "2022-2024各品牌销量及占有率 - 越野吊": "2022-2024 Brand Sales and Market Share - Rough-Terrain Cranes",
    "加拿大安大略市场与工况": "Ontario Market and Operating Conditions",
    "加拿大草原区域市场与工况": "Canadian Prairie Market and Operating Conditions",
    "加拿大草原省份市场与工况": "Canadian Prairie Market and Operating Conditions",
    "美国东北部市场与工况": "US Northeast Market and Operating Conditions",
    "美国东中部市场与工况": "US East-Central Market and Operating Conditions",
    "美国东中部市场": "US East-Central market",
    "美国东南部市场与工况": "US Southeast Market and Operating Conditions",
    "美国中南部市场与工况": "US South-Central Market and Operating Conditions",
    "美国中西上部市场与工况": "US Upper Midwest Market and Operating Conditions",
    "美国西海岸市场与工况": "US West Coast Market and Operating Conditions",
    "徐工XCR60_U/XCR75_U客户使用评价对标": "Customer Evaluation Benchmark - XCMG XCR60_U / XCR75_U",
    "徐工型号XCT35_U客户使用评价对标": "Customer Evaluation Benchmark - XCMG XCT35_U",
    "徐工型号XCT35_U性能指标对标": "Performance Benchmark - XCMG XCT35_U",
    "徐工型号XCT40_U客户使用评价对标": "Customer Evaluation Benchmark - XCMG XCT40_U",
    "徐工型号XCT40_U性能指标对标": "Performance Benchmark - XCMG XCT40_U",
    "徐工型号XCT60_U客户使用评价对标": "Customer Evaluation Benchmark - XCMG XCT60_U",
    "徐工型号XCT60_U性能指标对标": "Performance Benchmark - XCMG XCT60_U",
    "徐工型号XGC110U客户使用评价对标": "Customer Evaluation Benchmark - XCMG XGC110U",
    "徐工型号XGC110U性能指标对标": "Performance Benchmark - XCMG XGC110U",
    "住宅施工：北美大部分房屋为木质结构，需用起重机对框架、板材进行吊装和就位安装。": (
        "Residential construction: North American homes use wood-frame construction. "
        "Cranes lift and position structural frames, panels and other building components."
    ),
    "住宅施工：北美大部分房屋为木质结构，需用起重机对框架、板材进行吊装和就位安装。\n典型工况：作业幅度要求远≥30m，吊重量1000lb。": (
        "Residential construction: North American homes use wood-frame construction. "
        "Cranes lift and position structural frames and panels. Typical requirements include "
        "an operating radius of at least 30 m and a 1,000-lb load."
    ),
    "区域范围：马萨诸塞州、缅因州、新罕布什尔州等，区域特点：老城区更新、高架作业多，空间限制大。": (
        "Regional scope: Massachusetts, Maine and New Hampshire. Older urban districts, "
        "frequent elevated work and constrained jobsites favor compact machines with precise controls."
    ),
    "区域范围：伊利诺伊、俄亥俄、印第安纳、密歇根等州，区域特点：城市集中、法规严格、电力/广告/通信高空作业多。": (
        "Regional scope: Illinois, Ohio, Indiana and Michigan. Dense urban areas, strict regulations "
        "and frequent aerial work for utilities, signage and telecommunications shape equipment demand."
    ),
    "区域范围：佛罗里达州、佐治亚州、南/北卡罗来纳州、阿拉巴马州，区域特点：平原地貌、房建旺盛、环境复杂。": (
        "Regional scope: Florida, Georgia, North Carolina, South Carolina and Alabama. Flat terrain, "
        "strong building-construction demand and varied environmental conditions define the market."
    ),
    "区域范围：加利福尼亚、华盛顿、俄勒冈州。区域特点：加州沙土、高温（＞40℃）；华盛顿州雨林、湿地、多雨丘陵，公路、桥梁、建筑等施工较多。": (
        "Regional scope: California, Washington and Oregon. California combines sandy soils and "
        "temperatures above 40°C; Washington adds rain forest, wetland and hilly conditions with "
        "substantial road, bridge and building construction."
    ),
    "徐工型号XCR60_U：在售主打产品XCR60_U在显性参数和配置方面优于竞争对手，在产品软文资料方面仍需优化提升。": (
        "XCR60_U is XCMG's primary model in this class. Its published specifications and equipment "
        "package compare favorably with competitors, while sales literature still requires improvement."
    ),
    "徐工型号XCR75_U：在售主打产品XCR75_U在显性参数和配置方面优于竞争对手，在产品软文资料方面仍需优化提升。": (
        "XCR75_U is XCMG's primary model in this class. Its published specifications and equipment "
        "package compare favorably with competitors, while sales literature still requires improvement."
    ),
    "徐工型号XCR130_U：在售主打产品XCR130_U在核心参数和配置方面优于竞争对手，在底盘匹配品类和数量方面需进一步提升。": (
        "XCR130_U is XCMG's primary model in this class. Its core specifications and equipment package "
        "compare favorably with competitors; the range and number of compatible carrier configurations "
        "should be expanded."
    ),
    "徐工型号XCT35_U：在售主打产品XCT35_U在核心参数和配置方面优于竞争对手，在底盘匹配品类和数量方面需进一步提升。": (
        "XCT35_U is XCMG's primary model in this class. Its core specifications and equipment package "
        "compare favorably with competitors; the range and number of compatible carrier configurations "
        "should be expanded."
    ),
    "徐工型号XCT40_U：在售主打产品XCT40_U在核心参数和配置方面优于竞争对手，在底盘匹配品类和数量方面需进一步提升。": (
        "XCT40_U is XCMG's primary model in this class. Its core specifications and equipment package "
        "compare favorably with competitors; the range and number of compatible carrier configurations "
        "should be expanded."
    ),
    "徐工型号XCT60_U：在售主打产品XCT60_U在核心参数和配置方面优于竞争对手，在底盘匹配品类和数量方面需进一步提升。": (
        "XCT60_U is XCMG's primary model in this class. Its core specifications and equipment package "
        "compare favorably with competitors; the range and number of compatible carrier configurations "
        "should be expanded."
    ),
    "徐工型号XCA150_U：在售主打产品XCA150_U在显性参数和配置方面优于竞争对手，在产品操控性能、作业效率方面对比标杆仍需优化提升。": (
        "XCA150_U is XCMG's primary model in this class. Its published specifications and equipment "
        "package compare favorably with competitors, while control performance and jobsite efficiency "
        "still trail the benchmark."
    ),
    "徐工型号XCA275_U：在售主打产品XCA275_U在显性参数和配置方面优于竞争对手，在产品操控性能、作业效率方面对比标杆仍需优化提升。": (
        "XCA275_U is XCMG's primary model in this class. Its published specifications and equipment "
        "package compare favorably with competitors, while control performance and jobsite efficiency "
        "still trail the benchmark."
    ),
    "徐工口碑：\n产品性能卓越：整机起重性能高于行业最高水平且更加节能。其综合性能领先竞争对手。\n品牌2口碑：\n口碑1：\nGrove起重机技术太老了，配置还是十年前的，虽然没什么问题，但是有时我不得不自己改装加一些功能配置。": (
        "XCMG customer feedback: lifting performance and energy efficiency are viewed as competitive. "
        "Competitor feedback: Grove machines are considered reliable, but some customers regard the "
        "technology and equipment package as dated and add functions through local modifications."
    ),
    "徐工口碑：\n徐工40吨通用底盘起重机像来自欧洲全地面起重机一样，U型臂很结实，它其实更像45-50美吨产品，很划算。\n品牌2口碑：\nNational的40美吨Boomtruck是他们的经典产品了，虽然配置简单，但是很可靠，他们可以根据我们的需要选择美国的几乎任一主流品牌的底盘，我们附近PeterBilt口碑不错，这是我选择它的原因之一。": (
        "XCMG customer feedback: the 40-USt boom truck has a robust U-shaped boom and is perceived to "
        "deliver lifting capability closer to a 45-50-USt machine at an attractive price. Competitor "
        "feedback: National's 40-USt boom truck is valued for reliability and broad compatibility with "
        "mainstream North American chassis brands, including Peterbilt."
    ),
    "徐工口碑：\n徐工40美吨boom truck在Tree Guys也是比较Famous，他们改了不少东西，之前早期故障多，现在少一些了，我买了2台，都是用来吊树木的。\n品牌2口碑：\nNational的40吨Boom truck不管上车和底盘操作、维修简单，我们不是专业的起重机操作者，我们需要的是简单的操作，便捷的服务。": (
        "XCMG customer feedback: the 40-USt boom truck is established among tree-service contractors; "
        "early reliability issues have reportedly declined after product updates. Competitor feedback: "
        "National is favored by non-specialist operators for simple upper-structure and chassis controls, "
        "straightforward maintenance and accessible service support."
    ),
    "徐工口碑：\n徐工60美吨boomtruck，U型臂很结实，动作稳。组合式平衡重可以全配重转场，支腿支持多个位置支撑作业，很方便，性能很高，触摸屏操作便捷。\n品牌2口碑：\nNBT60XL是National的新产品，一如既往的简单可靠，另外配置提升不少，支腿还可以在多个位置支撑作业，很方便。": (
        "XCMG customer feedback: the 60-USt boom truck combines a robust U-shaped boom, stable motions, "
        "modular counterweight, multiple outrigger positions and an intuitive touchscreen. Competitor "
        "feedback: National's NBT60XL retains simple, reliable operation while adding a stronger equipment "
        "package and multiple outrigger positions."
    ),
    "徐工口碑：\n徐工XCT60_U我这车性价比很高，和我原来买的80-90吨汽车吊出勤率要高，上路方便。\n品牌2口碑：\nNBT60XL这车还不错，我比较认可，性能很稳定。": (
        "XCMG customer feedback: XCT60_U is viewed as cost-effective, easy to road and capable of higher "
        "utilization than some previously owned 80-90-USt truck cranes. Competitor feedback: National's "
        "NBT60XL is recognized for stable performance."
    ),
    "徐工口碑：\n我们公司主要承包当地工厂，用275主要是建筑施工，这台车吊装性能很高，功能配置很多用着不错。\n目前有一些问题，主要是液电的，操纵室翻转有时没有，取力偶尔挂不上，希望可靠性能更好一些，车能用，但是解决好这些问题就更好了。": (
        "XCMG customer feedback: XCA275_U provides strong lifting performance and a comprehensive equipment "
        "package for industrial and building construction. Reported improvement needs concern hydraulic and "
        "electrical reliability, intermittent cab-tilt operation and occasional power-take-off engagement."
    ),
    "我公司底盘匹配品类少， 匹配多品类底盘，覆盖北美重点销售区域需求。\n布局一款35吨产品": (
        "Current gap: XCMG supports too few carrier-chassis options. Expand compatibility across mainstream "
        "North American chassis brands and add a 35-USt model for priority sales regions."
    ),
    "我公司底盘匹配品类少， 匹配多品类底盘，覆盖北美重点销售区域需求。\n布局一款40吨产品": (
        "Current gap: XCMG supports too few carrier-chassis options. Expand compatibility across mainstream "
        "North American chassis brands and add a 40-USt model for priority sales regions."
    ),
    "XCT45_U性能覆盖行业45吨，与竞品NBT50系列相当，价格低15%。\n布局一款45吨产品": (
        "XCT45_U provides lifting capability comparable with the National NBT50 series at an indicated "
        "price approximately 15% lower. Portfolio action: add a 45-USt model."
    ),
    "在40美吨XCT40_U基础上升级开发45美吨通用底盘起重机，相比40美吨租赁利润更高，为市场客户提供更多选择。主要变化包括平衡重增加，增加不同支腿跨距组合下起重性能。": (
        "Develop a 45-USt boom truck from the XCT40_U platform to improve rental revenue potential and "
        "broaden customer choice. Key changes include additional counterweight and updated load charts for "
        "multiple outrigger spans."
    ),
    "研发目的：快速升级45美吨通用底盘起重机，相比40美吨租赁利润更高，同时边贡增加，满足市场对徐工45美吨产品需求；": (
        "Development objective: rapidly introduce a 45-USt boom truck with stronger rental-revenue potential "
        "and a broader operating envelope than the 40-USt model, addressing customer demand for an XCMG "
        "product in this class."
    ),
    "45美吨通用底盘起重机(市场导入)\n研发目的：快速升级45美吨通用底盘起重机，相比40美吨租赁利润更高，同时边贡增加，满足市场对徐工45美吨产品需求；\n产品方案：在XCT40_U基础上升级研发，增加平衡重提升作业性能3-5%，支腿支持多跨距组合，底盘和XCT40_U相同；\n售价目标：徐工销售当地售价参考同吨位机型，相比我公司40美吨增加1.5万-2万美元；\n完成时间：2025年完成认证和上市，预计2026年初完成市场导入，具备上市状态。": (
        "45-USt boom truck market-introduction plan. Objective: upgrade the XCT40_U platform to address "
        "demand for a higher-revenue 45-USt rental product. Proposed changes: add counterweight for an "
        "estimated 3-5% lifting-performance improvement, provide multiple outrigger-span configurations and "
        "retain the XCT40_U carrier platform. Historical price target: US$15,000-US$20,000 above the 40-USt "
        "model. The source plan targeted certification in 2025 and market introduction in early 2026; current "
        "completion status requires confirmation."
    ),
    "徐工口碑：\n我们公司主要承包当地工厂，用275主要是建筑施工，这台车吊装性能很高，功能配置很多用着不错。\n目前有一些问题，主要是液电的，操纵室翻转有时没有，取力偶尔挂不上，希望可靠性能更好一些，车能用，但是解决好这些问题就更好了。\n品牌2口碑：利勃海尔车很可靠、我新买这台车很先进，智能化程度很高，我遇到过一些问题，不过他们很快给我解决了。": (
        "XCMG customer feedback: XCA275_U provides strong lifting performance and a comprehensive equipment "
        "package for industrial and building construction. Reported improvement needs concern hydraulic and "
        "electrical reliability, intermittent cab-tilt operation and occasional power-take-off engagement. "
        "Competitor feedback: the Liebherr benchmark is regarded as reliable and technologically advanced, "
        "with responsive support when issues occur."
    ),
}


def _clean_crane_english(value: str) -> str:
    text = deterministic_cleanup(value)
    replacements = (
        (" ' s", "'s"),
        (" ' S", "'s"),
        ("Fuck Crane.", "Truck-mounted crane"),
        ("Tablet distribution", "Product-class mix"),
        ("Possession rate", "Market share"),
        ("Occupancy rate", "Market share"),
        ("occupancy rates", "market shares"),
        ("occupancy rate", "market share"),
        ("market occupancy", "market share"),
        ("Sales price/$ million", "Sales price (US$10,000)"),
        ("Sales price / $ million", "Sales price (US$10,000)"),
        ("Markets and Works", "Market and Operating Conditions"),
        ("Market and Works", "Market and Operating Conditions"),
        ("Market and Work", "Market and Operating Conditions"),
        ("customer usage evaluation benchmark", "Customer Evaluation Benchmark"),
        ("performance benchmarking", "Performance Benchmark"),
        ("obvious parameters", "published specifications"),
        ("seller's hit product", "primary production model"),
        ("vendor's hit product", "primary production model"),
        ("XCMG type ", "XCMG "),
        ("United East Central Markets", "US East-Central market"),
        (", etc., regional characteristics:", ". Regional characteristics:"),
        ("electricity/advertising/communications high altitude", "frequent aerial work for utilities, signage and telecommunications"),
        ("well-building", "strong building-construction demand"),
        ("The operational situation can be covered", "The required work conditions are covered"),
        ("The operational situation partially meets the needs", "The machine partially covers the required work conditions"),
        ("Work situation to meet needs", "Supported work conditions"),
        ("The job situation can cover", "The required work conditions are covered"),
        ("The job situation is satisfactory", "The required work conditions are covered"),
        ("Job conditions are satisfactory", "The required work conditions are covered"),
        ("axle charge", "axle load"),
        ("nudity axle load", "unladen axle load"),
        ("living capacity", "lifting capacity"),
        ("balance weight", "counterweight"),
        ("Variable counterweight", "Variable counterweight system"),
        ("main arm", "main boom"),
        ("secondary arm", "jib"),
        ("arm length", "boom length"),
        ("swing scale brakes", "proportional swing brake"),
        ("swing scale brake", "proportional swing brake"),
        ("control smoothing", "smooth control"),
        ("operation smoothing", "smooth operation"),
        ("manipulation, smoothing", "controls and smooth operation"),
        ("at high altitude", "at height"),
        ("high altitude operations", "lifting at height"),
        ("high altitude stability", "stability during lifting at height"),
        ("writing buildings", "office buildings"),
        ("seattopator cofort", "operator comfort"),
        ("Oporator cofort", "operator comfort"),
        ("XCMG logo", "XCMG customer feedback"),
        ("product sales literature", "sales and technical literature"),
        ("force-limiters", "rated-capacity limiter"),
        ("Machine reloads the jobsite level", "The machine can travel with a load between work positions"),
        ("main boom maximum crime height", "maximum main-boom lifting height"),
        ("high climate change", "wide seasonal temperature variation"),
        ("high-temperature dryness", "hot, dry conditions"),
        ("high urban construction", "intensive urban construction"),
        ("State of Agriculture", "agricultural production"),
        ("cold and cold weather", "cold winters"),
        ("old energy infrastructure", "aging energy infrastructure"),
        ("Construction scene and application description", "Application details"),
        ("Construction scene description", "Application details"),
        ("Construction scene", "Jobsite application"),
        ("customer groups", "customer segments"),
        ("customer group", "customer segment"),
        ("United States Middle West Upper Markets", "US Upper Midwest Market and Operating Conditions"),
        ("climate humid heat", "hot and humid climate"),
        ("California Sand", "California sandy soils"),
        ("Rain Hills", "rainy, hilly terrain"),
        ("Rainforests, Wetlands, rainy, hilly terrain", "rain forests, wetlands and rainy, hilly terrain"),
        ("Rainforest, Wetlands, Heavy rainy, hilly terrain", "rain forests, wetlands and steep, rainy terrain"),
        ("The application is supported, but", "The machine covers the core application, but"),
        ("The application is supported, while", "The machine covers the core application, while"),
        ("The application is supported, with", "The machine covers the core application, with"),
        ("The application is supported.", "The machine covers the application requirements."),
        ("1 set of 30 tons of products", "One 30-USt model in the current portfolio"),
        ("boom truck up to 35 t product segment", "Product segment: boom trucks up to 35 USt"),
        ("boom truck 40-up to 45 t product segment", "Product segment: 40-45-USt boom trucks"),
        ("boom truck 50 t and above product segment", "Product segment: boom trucks at 50 USt and above"),
        ("all-terrain crane 100-150 t product segment", "Product segment: 100-150-USt all-terrain cranes"),
        ("all-terrain crane 200-300 t product segment", "Product segment: 200-300-USt all-terrain cranes"),
        ("all-terrain crane 220-300 t product segment", "Product segment: 220-300-USt all-terrain cranes"),
        ("rough-terrain crane 60-75 t product segment", "Product segment: 60-75-USt rough-terrain cranes"),
        ("rough-terrain crane 120-130 t product segment", "Product segment: 120-130-USt rough-terrain cranes"),
        ("Comparison conclusion:.", "Comparison conclusion:"),
        ("High Temperature (>40°C)", "temperatures above 40°C"),
        ("mainly for natural disaster relief, bridge laying, engineering, etc.", "supporting disaster response, temporary bridge installation and civil construction."),
        ("construction of roads, bridges, construction, etc.", "supporting road, bridge and building construction."),
        ("Yes, ? deg", "Yes; angle not specified"),
        ("Yes, ?", "Yes; value not specified"),
    )
    for source, target in replacements:
        text = text.replace(source, target)
    text = re.sub(r"(\d+(?:\.\d+)?)\s+per cent\b", r"\1%", text, flags=re.I)
    text = re.sub(r"\bXCMG model\s+", "XCMG ", text, flags=re.I)
    text = re.sub(r"\b(XC[RTG]\d+)\s+U\b", r"\1_U", text)
    text = re.sub(
        r"Regional scope:\s*(.+?)\.\s*Regional characteristics:\s*",
        r"Region: \1. Market and operating context: ",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"Regional scope:\s*(.+),\s*regional characteristics:\s*",
        r"Region: \1. Market and operating context: ",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"(.+?)\s+have regional characteristics:\s*",
        r"Region: \1. Market and operating context: ",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"^(rough-terrain crane|all-terrain crane|boom truck|crawler crane)\s+(.+?)\s+product segment\.$",
        lambda match: f"Product segment: {match.group(1)}, {match.group(2)}.",
        text,
        flags=re.I,
    )
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def _en(value: Any) -> str:
    text = str(value or "").strip()
    exact = (
        CRANE_ENGLISH_OVERRIDES.get(text)
        or MANUAL_OVERRIDES.get(text)
        or generated_manual_override(text)
        or EN_TRANSLATIONS.get(text)
    )
    if exact:
        return _clean_crane_english(exact)
    fallback = text.replace("现有产品", "Current products").replace("新品", "New products")
    category_terms = {
        "越野轮胎起重机": "rough-terrain crane",
        "全地面起重机": "all-terrain crane",
        "通用底盘起重机": "boom truck",
        "履带起重机": "crawler crane",
    }
    for source_term, target_term in category_terms.items():
        fallback = fallback.replace(source_term, target_term)
    fallback = re.sub(r"(crane|truck)(?=\d)", r"\1 ", fallback)
    fallback = re.sub(r"(\d+)\s*[~—–-]\s*(\d+)吨产品段", r"\1-\2 t product segment", fallback)
    fallback = re.sub(r"(\d+)\s*[~—–-]\s*(\d+)吨级", r"\1-\2 t class", fallback)
    fallback = re.sub(r"(\d+)吨及以下产品段", r"up to \1 t product segment", fallback)
    fallback = re.sub(r"(\d+)吨及以上产品段", r"\1 t and above product segment", fallback)
    fallback = re.sub(r"(\d+)吨产品段", r"\1 t product segment", fallback)
    fallback = re.sub(r"(\d+)吨产品", r"\1 t product", fallback)
    return _clean_crane_english(fallback)

STATUS_COPY = {
    "historical": ("历史数据", "Historical data"),
    "current-at-source-date": ("截至2025-07判断", "Assessment as of 2025-07"),
    "plan": ("规划 / 待验证", "Plan / validation pending"),
}

SECTION_LABELS = {
    "macro": "市场环境",
    "market-volume": "市场规模",
    "competition": "品牌格局",
    "regional-demand": "区域需求",
    "boom-truck": "通用底盘",
    "all-terrain": "全地面",
    "rough-terrain": "越野轮胎",
    "crawler": "履带起重机",
    "portfolio": "产品型谱",
    "roadmap": "改进路线",
    "go-to-market": "市场与服务",
}

SECTION_LABELS_EN = {
    "macro": "Market Environment",
    "market-volume": "Market Size",
    "competition": "Competitive Landscape",
    "regional-demand": "Regional Demand",
    "boom-truck": "Boom Trucks",
    "all-terrain": "All-Terrain Cranes",
    "rough-terrain": "Rough-Terrain Cranes",
    "crawler": "Crawler Cranes",
    "portfolio": "Product Portfolio",
    "roadmap": "Improvement Roadmap",
    "go-to-market": "Market and Service",
}

SLIDE_TITLE_OVERRIDES = {
    2: "北美宏观环境及其对起重机业务的影响",
    3: "北美起重机销量与产品类别结构",
    4: "通用底盘与越野轮胎起重机品牌份额",
    5: "全地面与履带起重机品牌份额",
    6: "各产品类别主要竞争标杆与市场定位",
    7: "北美起重机区域需求分布",
    8: "北美区域差异与产品适应性",
    9: "北美区域需求与配置策略",
}

SLIDE_TITLE_OVERRIDES_EN = {
    2: "North American Macro Environment and Business Implications",
    3: "North American Crane Sales and Product-Class Mix",
    4: "Boom-Truck and Rough-Terrain Crane Brand Share",
    5: "All-Terrain and Crawler-Crane Brand Share",
    6: "Competitive Benchmarks and Positioning by Product Class",
    7: "Regional Distribution of North American Crane Demand",
    8: "Regional Differences and Product Adaptation in North America",
    9: "Regional Demand and Equipment Strategy",
}

IMAGE_CAPTION_OVERRIDES = {
    7: (
        "2024年加拿大越野轮胎起重机销量分布",
        "2024年美国越野轮胎起重机销量分布",
        "2024年美国全地面起重机销量分布",
        "2024年美国履带起重机销量分布",
        "2024年美国通用底盘起重机销量分布",
    ),
}

IMAGE_CAPTION_OVERRIDES_EN = {
    7: (
        "2024 Canadian rough-terrain crane sales distribution",
        "2024 US rough-terrain crane sales distribution",
        "2024 US all-terrain crane sales distribution",
        "2024 US crawler-crane sales distribution",
        "2024 US boom-truck sales distribution",
    ),
}

PARAGRAPH_OVERRIDES = {
    81: (
        (
            "越野轮胎起重机占起重机产品线销量34.1%，主流吨级包括60吨、75吨、100吨、130吨，主需求吨级主要集中在50吨以上。",
            "Rough-terrain cranes account for 34.1% of crane product-line sales. The primary classes are 60, 75, 100 and 130 USt, with most demand concentrated above 50 USt.",
        ),
        (
            "0-16.9吨占比4.2%，17-24.9吨市场占比3.6%，25-34.9吨市场占比7.6%，35-39.9吨占比2.3%，40-49.9占比0.7%。",
            "The 0-16.9 USt class represents 4.2% of the market; 17-24.9 USt, 3.6%; 25-34.9 USt, 7.6%; 35-39.9 USt, 2.3%; and 40-49.9 USt, 0.7%.",
        ),
        (
            "50吨以下市场整体占比在18.4%，但需求分散，各吨级占比小，储备50美吨，根据市场需求推进。",
            "Classes below 50 USt account for 18.4% in total, but demand is fragmented. Retain a 50-USt concept and advance it only as market demand develops.",
        ),
        (
            "现有型谱覆盖XCR60_U、XCR75_U、XCR100_U和XCR130_U；165美吨产品仍处于论证阶段。",
            "The current portfolio covers XCR60_U, XCR75_U, XCR100_U and XCR130_U; a 165-USt model remains under evaluation.",
        ),
    ),
}

CLASS_INTRO = {
    "RT-60t": (
        "60-75吨级越野吊集中服务住宅施工、电力检修、油气与工业设施、道路桥梁等场景。材料同时覆盖区域工况、参配对比、客户口碑及可靠性、安全性、操控性、舒适性和维修性评价。",
        "The 60-75 t rough-terrain segment serves residential construction, utility maintenance, oil and gas, industrial facilities, roads and bridges. The evidence covers regional applications, specifications, customer feedback, reliability, safety, controllability, comfort and serviceability.",
    ),
    "RT-75t": (
        "60-75吨级越野吊集中服务住宅施工、电力检修、油气与工业设施、道路桥梁等场景。材料同时覆盖区域工况、参配对比、客户口碑及可靠性、安全性、操控性、舒适性和维修性评价。",
        "The 60-75 t rough-terrain segment serves residential construction, utility maintenance, oil and gas, industrial facilities, roads and bridges. The evidence covers regional applications, specifications, customer feedback, reliability, safety, controllability, comfort and serviceability.",
    ),
    "RT-100t": (
        "90-110吨级越野吊面向城市更新、工业厂房、电力和通信维护、自然灾害救援及大型工程。对标重点从单一吊重参数扩展到长臂覆盖、低温和高温适应、微动性、故障诊断与维保便利性。",
        "The 90-110 t rough-terrain segment supports urban renewal, industrial plants, utility and communications work, disaster response and large projects. Benchmarking extends beyond lift capacity to long-boom coverage, climate adaptation, fine control, diagnostics and serviceability.",
    ),
    "RT-130t": (
        "120-130吨级越野吊对应大型工业、能源、港口及重型基础设施吊装。页面保留区域与工况矩阵、XCR130_U参数配置对比、客户使用评价以及当时的产品定位和市场目标。",
        "The 120-130 t rough-terrain segment targets large industrial, energy, port and heavy-infrastructure lifts. The page retains the regional application matrix, XCR130_U comparison, customer-use evaluation, and the product positioning and market targets stated at the source date.",
    ),
    "RT-160t": (
        "该吨级材料属于165美吨越野吊产品规划，不是当前实机验证结论。页面用于说明北美大吨位需求、初步技术方案、型谱位置和计划节点，并与现有Excel数据缺口分开呈现。",
        "This class is represented by the planned 165-US-ton rough-terrain crane, not a verified current machine evaluation. The page shows demand, the initial technical concept, portfolio position and planned milestones separately from Excel data gaps.",
    ),
    "AT-150t": (
        "150吨级全地面起重机聚焦风电、能源、工业安装和大型基础设施。材料覆盖重点区域、客户任务、XCA150_U参配对比，以及安全、人性化、配重适应性、可靠性和伸缩效率的实机评价。",
        "The 150 t all-terrain segment focuses on wind, energy, industrial installation and major infrastructure. Evidence covers priority regions, customer tasks, XCA150_U comparisons, safety, ergonomics, counterweight flexibility, reliability and telescoping efficiency.",
    ),
}

SHARED_RESEARCH_NOTICES = {
    "RT-60t": {
        "shared_class": "RT-75t",
        "zh": (
            "本页与75吨级共用60-75吨级市场、区域需求、客户工况及实机评价资料（CR-81-85、CR-88-93）。"
            "XCR60_U的参数、标杆机型、售价及产品结论按本机型独立展示，见第86、94页。"
        ),
        "en": (
            "This page shares the 60-75-USt market, regional-demand, customer-application and field-evaluation research "
            "with the 75-USt page (CR-81-85 and CR-88-93). XCR60_U specifications, benchmark model, pricing and "
            "conclusions are presented separately on slides 86 and 94."
        ),
    },
    "RT-75t": {
        "shared_class": "RT-60t",
        "zh": (
            "本页与60吨级共用60-75吨级市场、区域需求、客户工况及实机评价资料（CR-81-85、CR-88-93）。"
            "XCR75_U的参数、标杆机型、售价及产品结论按本机型独立展示，见第87、95页。"
        ),
        "en": (
            "This page shares the 60-75-USt market, regional-demand, customer-application and field-evaluation research "
            "with the 60-USt page (CR-81-85 and CR-88-93). XCR75_U specifications, benchmark model, pricing and "
            "conclusions are presented separately on slides 87 and 95."
        ),
    },
}

CLASS_PAGE_SECTIONS = (
    (
        "market-insight",
        "吨级市场与竞争定位",
        "Market and Competitive Position",
        "先明确该吨级在北美起重机产品线中的需求位置、主流产品范围和竞争边界，再进入具体产品比较。",
        "Establishes the class's demand position, mainstream product range and competitive boundary in North America before moving into product-level comparison.",
    ),
    (
        "job-applications",
        "区域需求与典型施工任务",
        "Regional Demand and Typical Jobs",
        "按区域产业、气候、法规和施工任务展示真实应用条件，并把现场影像与对应作业要求放在同一处阅读。",
        "Connects regional industry, climate, regulation and job tasks with field imagery and the corresponding operating requirements.",
    ),
    (
        "engineering-insight",
        "参数、配置与实机评价",
        "Specifications, Equipment and Field Evaluation",
        "把纸面参数与配置对比、客户使用反馈和实机观察分开呈现，避免将参数优势直接等同于现场表现。",
        "Separates published specifications and equipment from customer feedback and field observations so paper strengths are not treated as field-performance proof.",
    ),
    (
        "product-positioning",
        "产品定位与推进计划",
        "Product Positioning and Program Plan",
        "保留资料形成时的价格定位、销量目标和产品计划；规划内容仅作为决策输入，不代表已经上市或完成验证。",
        "Retains source-date pricing, volume targets and product plans. Planned items are decision inputs, not evidence of launch or completed validation.",
    ),
)

REPORT_SECTIONS = [
    (
        "macro",
        "宏观环境与市场规模",
        "Macro Environment and Market Size",
        "从政策、经济、社会、技术、环境和法规六个维度解释北美起重机市场的约束与机会，并连接到销量、产品结构和经营风险。",
        "Explains the constraints and opportunities in the North American crane market across policy, economic, social, technological, environmental and legal dimensions, linked to volume, product mix and operating risk.",
        list(range(1, 4)),
    ),
    (
        "competition",
        "竞争格局与区域需求",
        "Competitive Landscape and Regional Demand",
        "按通用底盘、越野吊、全地面和履带吊拆分品牌份额，并结合美国和加拿大主要区域的产业结构、气候和法规差异。",
        "Breaks down share by boom truck, rough-terrain, all-terrain and crawler crane, then connects United States and Canada regional demand to industry structure, climate and regulation.",
        list(range(4, 10)),
    ),
    (
        "boom-truck",
        "通用底盘起重机产品线",
        "Boom-Truck Product Line",
        "完整保留35吨及以下、40-45吨和50吨以上产品段的区域场景、参数配置、客户评价、产品定位和当时目标。",
        "Retains regional applications, specification and equipment comparisons, customer evaluations, positioning and source-date targets for the up-to-35 t, 40-45 t and 50 t-plus segments.",
        list(range(10, 58)),
    ),
    (
        "all-terrain",
        "全地面起重机扩展分析",
        "All-Terrain Crane Expansion",
        "补充XCA275_U等未建立正式Excel吨级页的市场、区域、产品和客户评价；XCA150_U细节在对应吨级页展示。",
        "Adds the market, regional, product and customer evaluation for XCA275_U and other segments without a formal Excel class page. XCA150_U detail remains on its class page.",
        list(range(69, 81)),
    ),
    (
        "crawler",
        "履带起重机市场与产品评价",
        "Crawler-Crane Market and Product Evaluation",
        "覆盖履带吊销量结构、100吨级产品方案、核心参数、六性评价、客户反馈、价格定位和样机验证目标。",
        "Covers crawler-crane volume mix, the 100 t concept, specifications, six-characteristic evaluation, customer feedback, price positioning and prototype-validation targets.",
        list(range(120, 130)),
    ),
    (
        "portfolio",
        "产品型谱与竞争力提升",
        "Portfolio and Competitiveness Improvement",
        "把通用底盘、全地面、越野吊和履带吊的型谱覆盖、空白吨级、现有产品问题及跨产品线提升重点放在同一张路线图中。",
        "Brings portfolio coverage, missing classes, current-product issues and cross-line improvement priorities for boom trucks, all-terrain, rough-terrain and crawler cranes into one roadmap.",
        list(range(130, 143)),
    ),
    (
        "roadmap",
        "2025-2027产品路线图",
        "2025-2027 Product Roadmap",
        "按原资料保留新品定义、关键技术方案、售价目标和计划节点；这些内容全部标为规划，不能视为已经上市或完成验证。",
        "Retains new-product definitions, technical concepts, price targets and planned milestones. Every item is labelled as a plan and must not be read as launched or validated.",
        list(range(143, 153)),
    ),
    (
        "go-to-market",
        "市场、渠道、服务与本地化",
        "Market, Channel, Service and Localization",
        "展示市场机会、销售目标、产品进攻策略、经销网络、租赁客户、服务备件和美国本地组装规划，形成从产品到交付的闭环。",
        "Shows market opportunity, sales targets, product strategy, dealer network, rental accounts, service and parts, and U.S. assembly plans to connect product decisions to delivery.",
        list(range(153, 164)),
    ),
]


def esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def load_crane_insights() -> dict[str, Any]:
    slides = json.loads((OUTPUT_DIR / "slides.json").read_text(encoding="utf-8"))
    segments = json.loads((OUTPUT_DIR / "segment-map.json").read_text(encoding="utf-8"))
    evidence = json.loads((OUTPUT_DIR / "evidence.json").read_text(encoding="utf-8"))
    return {
        "slides": slides,
        "by_slide": {item["slide"]: item for item in slides},
        "segments": segments,
        "evidence": evidence,
    }


def _status_badge(status: str) -> str:
    zh, en = STATUS_COPY.get(status, (status, status))
    return f'<span class="sourceStatus {esc(status)}" data-en="{esc(en)}">{esc(zh)}</span>'


def _useful_text(record: dict[str, Any]) -> list[str]:
    ignored_exact = {
        "二、大区产业板块洞察",
        "二、大区产业板块洞察—北美",
        "二、大区产业板块洞察—美国和加拿大",
        "起重机产品线",
        "数据来源: AEM",
        "数据来源：AEM",
    }
    ignored_prefixes = ("2、核心产品线—", "2、核心产品线—越野轮胎起重机")
    items = []
    seen = set()
    for block in record["text_blocks"]:
        for part in re.split(r"\n(?=\S)", block["text"]):
            text = part.strip()
            if not text or text in ignored_exact or text.startswith(ignored_prefixes):
                continue
            if text.startswith("2.4 市场洞察分析-"):
                text = text.split("-", 1)[1].strip()
            elif text.startswith("2.6 产品线竞争力提升举措-"):
                text = text.split("-", 1)[1].strip()
            if re.fullmatch(r"\d{1,3}", text):
                continue
            key = re.sub(r"\s+", "", text)
            if key in seen:
                continue
            seen.add(key)
            items.append(text)
    return items


def _display_title(record: dict[str, Any]) -> str:
    if record["slide"] in SLIDE_TITLE_OVERRIDES:
        return SLIDE_TITLE_OVERRIDES[record["slide"]]
    table_labels = []
    for table in record.get("tables", []):
        rows = table.get("rows") or []
        if len(rows) != 1 or len(rows[0]) != 1:
            continue
        label = str(rows[0][0]).strip()
        if label and len(label) <= 30 and label not in table_labels:
            table_labels.append(label)
    if table_labels:
        return _clean_business_title(" · ".join(table_labels))
    candidates = _useful_text(record)
    preferred_tokens = (
        "徐工型号",
        "客户使用评价",
        "对比结论",
        "区域范围",
        "销量趋势",
        "市场洞察",
        "可售型谱",
        "市场营销",
        "服务能力",
        "当地化",
        "布局",
    )
    for text in candidates:
        if any(token in text for token in preferred_tokens):
            return _clean_business_title(text.split("：", 1)[0][:90])
    for text in candidates:
        if 6 <= len(text) <= 90:
            return _clean_business_title(text)
    return _clean_business_title(record["title"][:90])


def _clean_business_title(value: str) -> str:
    text = re.sub(r"^\s*\d+(?:\.\d+)+\s*", "", str(value)).strip()
    region = re.fullmatch(r"\d+\s*-\s*(.+?)\s*·\s*(美国|加拿大)", text)
    if region:
        return f"{region.group(2)}{region.group(1).strip()}市场与工况"
    replacements = (
        ("占有率分析及竞争对手锁定", "品牌份额与主要竞争对手"),
        ("市场洞察分析-", ""),
        ("市场营销-", ""),
        ("产品线竞争力提升举措-", ""),
        ("可售型谱分析——", ""),
    )
    for source, target in replacements:
        text = text.replace(source, target)
    return text.strip(" -—·") or "产品与市场分析"


def _paragraphs(record: dict[str, Any], limit: int | None = None) -> str:
    if record["slide"] in PARAGRAPH_OVERRIDES:
        values = PARAGRAPH_OVERRIDES[record["slide"]]
        if limit is not None:
            values = values[:limit]
        return "".join(
            f'<p lang="zh-CN" data-en="{esc(en)}">{esc(zh)}</p>'
            for zh, en in values
        )
    items = _useful_text(record)
    title = _display_title(record)
    filtered = [item for item in items if item != title]
    if limit is not None:
        filtered = filtered[:limit]
    paragraphs: list[tuple[str, str]] = []
    short_run: list[tuple[str, str]] = []
    for item in filtered:
        compact = re.sub(r"\s+", " ", item).strip()
        compact = re.sub(r"^\d+(?:\.\d+)+\s+", "", compact)
        compact = compact.replace("市场洞察分析-", "", 1).strip(" -—·")
        translated = re.sub(r"\s+", " ", _en(item)).strip()
        translated = re.sub(r"^\d+(?:\.\d+)+\s+", "", translated)
        if not compact or compact == title:
            continue
        is_short = len(compact) <= 45 and not re.search(r"[。！？；:]$", compact)
        if is_short:
            short_run.append((compact, translated))
            if sum(len(value[0]) for value in short_run) < 90:
                continue
        if short_run:
            paragraphs.append(
                ("；".join(value[0] for value in short_run) + "。", "; ".join(value[1] for value in short_run) + ".")
            )
            short_run = []
        if not is_short:
            paragraphs.append((compact, translated))
    if short_run:
        paragraphs.append(
            ("；".join(value[0] for value in short_run) + "。", "; ".join(value[1] for value in short_run) + ".")
        )
    return "".join(
        f'<p lang="zh-CN" data-en="{esc(en)}">{esc(zh)}</p>'
        for zh, en in paragraphs
    )


def _meaningful_table(table: dict[str, Any]) -> bool:
    rows = table.get("rows") or []
    nonempty = [str(cell).strip() for row in rows for cell in row if str(cell).strip()]
    if len(rows) >= 2 and len(nonempty) >= 4:
        return True
    return 1 <= len(nonempty) <= 2 and max((len(cell) for cell in nonempty), default=0) >= 80


def _render_table(table: dict[str, Any], slide_number: int, index: int) -> str:
    rows = table["rows"]
    width = max((len(row) for row in rows), default=0)
    if width == 0:
        return ""
    active_columns = [
        column
        for column in range(width)
        if any(column < len(row) and str(row[column]).strip() for row in rows)
    ]
    if not active_columns:
        return ""
    nonempty = [str(cell).strip() for row in rows for cell in row if str(cell).strip()]
    if len(nonempty) == 1:
        content = nonempty[0]
        return (
            f'<aside class="craneSourceCallout" data-table-slide="{slide_number}" data-table-index="{index}">'
            f'<p data-en="{esc(_en(content))}">{esc(content)}</p></aside>'
        )

    first_row_values = [
        str(rows[0][column]).strip() if column < len(rows[0]) else ""
        for column in active_columns
    ]
    first_row_nonempty = [value for value in first_row_values if value]
    header_index = 0
    caption = ""
    if len(rows) > 1 and len(first_row_nonempty) == 1:
        second_row_values = [
            str(rows[1][column]).strip() if column < len(rows[1]) else ""
            for column in active_columns
        ]
        if len([value for value in second_row_values if value]) >= 2:
            caption = first_row_nonempty[0]
            header_index = 1
    headers = [
        (str(rows[header_index][column]).strip() if column < len(rows[header_index]) else "") or "补充信息"
        for column in active_columns
    ]
    rendered_rows = []
    for row_index, row in enumerate(rows[header_index:], start=header_index):
        cells = [str(row[column]) if column < len(row) else "" for column in active_columns]
        if row_index == header_index:
            rendered_rows.append(
                "<tr>" + "".join(
                    f'<th data-en="{esc(_en(cell))}">{esc(cell)}</th>' for cell in cells
                ) + "</tr>"
            )
            continue
        rendered_rows.append(
            "<tr>" + "".join(
                f'<td data-label-zh="{esc(headers[cell_index])}" '
                f'data-label-en="{esc(_en(headers[cell_index]))}" '
                f'data-en="{esc(_en(cell))}">{esc(cell)}</td>'
                for cell_index, cell in enumerate(cells)
            ) + "</tr>"
        )
    if len(active_columns) >= 11:
        width_class = " wide ultra-wide"
    elif len(active_columns) >= 7:
        width_class = " wide"
    else:
        width_class = ""
    caption_html = (
        f'<caption data-en="{esc(_en(caption))}">{esc(caption)}</caption>'
        if caption
        else ""
    )
    return (
        f'<div class="craneSourceTable{width_class}" data-table-slide="{slide_number}" data-table-index="{index}" '
        f'data-column-count="{len(active_columns)}">'
        f'<table>{caption_html}<thead>{rendered_rows[0]}</thead><tbody>'
        + "".join(rendered_rows[1:])
        + "</tbody></table></div>"
    )


def _chart_values(chart: dict[str, Any]) -> list[float]:
    return [
        float(value)
        for series in chart.get("series", [])
        for value in series.get("values", [])
        if isinstance(value, (int, float)) and math.isfinite(value)
    ]


def _render_pie(chart: dict[str, Any], chart_id: str) -> str:
    categories = chart.get("categories") or []
    series = (chart.get("series") or [{}])[0]
    values = [float(value or 0) for value in series.get("values", [])]
    if not categories or not values or sum(values) <= 0:
        return ""
    colors = ["#0a5ca4", "#f5b400", "#279b7d", "#e2605f", "#7656c8", "#6d8498", "#a97112", "#2d7257"]
    total = sum(values)
    cursor = 0.0
    stops = []
    legend = []
    for index, (category, value) in enumerate(zip(categories, values)):
        share = value / total * 100
        color = colors[index % len(colors)]
        stops.append(f"{color} {cursor:.3f}% {cursor + share:.3f}%")
        legend.append(
            f'<li tabindex="0" data-chart-key="{esc(category)}"><i style="background:{color}"></i>'
            f'<span data-en="{esc(_en(category))}">{esc(category)}</span><b>{share:.1f}%</b><small>{value:,.0f}</small></li>'
        )
        cursor += share
    return (
        f'<div class="insightDonut" data-chart-id="{esc(chart_id)}">'
        f'<div class="donutGraphic" style="--donut:{esc(",".join(stops))}"><span>{total:,.0f}</span></div>'
        f'<ul>{"".join(legend)}</ul></div>'
    )


def _render_columns(chart: dict[str, Any], chart_id: str) -> str:
    categories = chart.get("categories") or []
    series = chart.get("series") or []
    values = _chart_values(chart)
    if not categories or not series or not values:
        return ""
    maximum = max(abs(value) for value in values) or 1
    colors = ["#0a5ca4", "#f5b400", "#279b7d", "#e2605f", "#7656c8", "#6d8498"]
    groups = []
    max_categories = 18
    for category_index, category in enumerate(categories[:max_categories]):
        bars = []
        for series_index, item in enumerate(series[:6]):
            raw = item.get("values", [])
            value = raw[category_index] if category_index < len(raw) else None
            if not isinstance(value, (int, float)):
                continue
            height = max(2.0, abs(float(value)) / maximum * 100)
            color = colors[series_index % len(colors)]
            label = item.get("name") or "Series"
            label_en = _en(label)
            bars.append(
                f'<i tabindex="0" style="height:{height:.2f}%;background:{color}" '
                f'data-label="{esc(label_en)}" data-value="{float(value):g}" title="{esc(label_en)}: {float(value):g}"></i>'
            )
        groups.append(
            f'<div class="insightColumnGroup"><div>{"".join(bars)}</div><span data-en="{esc(_en(category))}">{esc(category)}</span></div>'
        )
    legend = "".join(
        f'<span><i style="background:{colors[index % len(colors)]}"></i>'
        f'<em data-en="{esc(_en(item.get("name") or "Series"))}">{esc(item.get("name") or "Series")}</em></span>'
        for index, item in enumerate(series[:6])
    )
    return (
        f'<div class="insightColumns" data-chart-id="{esc(chart_id)}"><div class="columnPlot">'
        f'{"".join(groups)}</div><div class="chartLegend">{legend}</div></div>'
    )


def _render_scalar_comparison(chart: dict[str, Any], chart_id: str) -> str:
    series = chart.get("series") or []
    items = []
    for index, item in enumerate(series):
        values = item.get("values") or []
        if len(values) != 1 or not isinstance(values[0], (int, float)):
            continue
        name = re.sub(r"\s+", " ", str(item.get("name") or "")).strip()
        if not name:
            continue
        items.append((name, float(values[0]), index))
    if len(items) < 2:
        return ""
    maximum = max(abs(value) for _name, value, _index in items) or 1
    rows = []
    for name, value, index in items:
        width = max(1.5, abs(value) / maximum * 100)
        color = "#f5b400" if index == 0 else "#075a9f"
        value_label = f"{value * 100:.1f}%" if abs(value) <= 1 else f"{value:g}"
        rows.append(
            '<div class="comparisonRow" tabindex="0">'
            f'<b data-en="{esc(_en(name))}">{esc(name)}</b>'
            f'<span><i style="width:{width:.2f}%;background:{color}"></i></span>'
            f'<strong>{esc(value_label)}</strong></div>'
        )
    return (
        f'<div class="insightComparison" data-chart-id="{esc(chart_id)}">'
        '<h4 data-en="Market share comparison">市场份额对比</h4>'
        f'{"".join(rows)}</div>'
    )


def _chart_extent(values: list[float]) -> tuple[float, float]:
    low, high = min(values), max(values)
    span = high - low
    padding = span * 0.22 if span else max(abs(high) * 0.15, 1.0)
    return low - padding, high + padding


def _render_scatter(chart: dict[str, Any], chart_id: str, slide_number: int) -> str:
    points = []
    for index, item in enumerate(chart.get("series") or []):
        x_values = item.get("x_values") or []
        y_values = item.get("y_values") or item.get("values") or []
        if not x_values or not y_values:
            continue
        if not isinstance(x_values[0], (int, float)) or not isinstance(y_values[0], (int, float)):
            continue
        points.append({
            "name": re.sub(r"\s+", " ", str(item.get("name") or "")).strip(),
            "x": float(x_values[0]),
            "y": float(y_values[0]),
            "index": index,
        })
    if len(points) < 2:
        return ""
    x_low, x_high = _chart_extent([point["x"] for point in points])
    y_low, y_high = _chart_extent([point["y"] for point in points])
    left, right, top, bottom = 90.0, 720.0, 36.0, 310.0
    x_pos = lambda value: left + (value - x_low) / (x_high - x_low) * (right - left)
    y_pos = lambda value: bottom - (value - y_low) / (y_high - y_low) * (bottom - top)
    grid = []
    for step in range(5):
        ratio = step / 4
        x = left + ratio * (right - left)
        y = bottom - ratio * (bottom - top)
        x_value = x_low + ratio * (x_high - x_low)
        y_value = y_low + ratio * (y_high - y_low)
        grid.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}"/><text x="{x:.1f}" y="334" text-anchor="middle">{x_value:.1f}</text>')
        grid.append(f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}"/><text x="80" y="{y + 4:.1f}" text-anchor="end">{y_value * 100:.1f}%</text>')
    marks = []
    legend = []
    for point in points:
        color = "#f5b400" if point["index"] == 0 else "#075a9f"
        px, py = x_pos(point["x"]), y_pos(point["y"])
        name_en = _en(point["name"])
        value_label = f'{point["x"]:.1f} / {point["y"] * 100:.1f}%'
        anchor = "start" if px < (left + right) / 2 else "end"
        label_x = px + 12 if anchor == "start" else px - 12
        marks.append(
            f'<g class="scatterPoint" tabindex="0" data-chart-key="{esc(name_en)}">'
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="9" fill="{color}"/>'
            f'<text x="{label_x:.1f}" y="{py - 5:.1f}" text-anchor="{anchor}" class="pointName" data-en="{esc(name_en)}">{esc(point["name"])}</text>'
            f'<text x="{label_x:.1f}" y="{py + 11:.1f}" text-anchor="{anchor}" class="pointValue">{esc(value_label)}</text>'
            f'<title>{esc(name_en)}: {esc(value_label)}</title></g>'
        )
        legend.append(f'<span><i style="background:{color}"></i><b data-en="{esc(name_en)}">{esc(point["name"])}</b><small>{esc(value_label)}</small></span>')
    return (
        f'<div class="insightScatter" data-chart-id="{esc(chart_id)}">'
        '<header><h4 data-en="Price and market-position comparison">价格与市场位置对比</h4>'
        '<p data-en="Horizontal axis: reported selling-price index; vertical axis: recorded market share. Hover or focus a point for its values.">横轴为资料记录售价指标，纵轴为对应市场占有率；悬停或聚焦点位可查看数值。</p></header>'
        f'<svg viewBox="0 0 760 365" role="img" aria-label="第{slide_number}页价格与市场位置散点图"><g class="scatterGrid">{"".join(grid)}</g>'
        f'<line class="scatterAxis" x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}"/><line class="scatterAxis" x1="{left}" y1="{top}" x2="{left}" y2="{bottom}"/>'
        '<text class="axisTitle" x="405" y="360" text-anchor="middle" data-en="Reported selling-price index">资料记录售价指标</text>'
        '<text class="axisTitle" transform="translate(18 175) rotate(-90)" text-anchor="middle" data-en="Market share">市场占有率</text>'
        f'{"".join(marks)}</svg><div class="scatterLegend">{"".join(legend)}</div></div>'
    )


def _render_bubble(chart: dict[str, Any], chart_id: str) -> str:
    series = (chart.get("series") or [{}])[0]
    x_values = [float(value) for value in series.get("x_values") or [] if isinstance(value, (int, float))]
    y_values = [float(value) for value in series.get("y_values") or series.get("values") or [] if isinstance(value, (int, float))]
    bubble_sizes = [float(value) for value in series.get("bubble_sizes") or [] if isinstance(value, (int, float))]
    if not (len(x_values) == len(y_values) == len(bubble_sizes) and len(x_values) >= 2):
        return ""
    labels_zh = ["通用底盘", "越野吊", "全地面", "履带吊"] if len(x_values) == 4 else [f"业务{i + 1}" for i in range(len(x_values))]
    labels_en = ["Boom truck", "Rough-terrain", "All-terrain", "Crawler"] if len(x_values) == 4 else [f"Business {i + 1}" for i in range(len(x_values))]
    left, right, top, bottom = 70.0, 720.0, 30.0, 330.0
    max_size = max(bubble_sizes) or 1
    grid = []
    for step in range(6):
        value = step * 2
        x = left + value / 10 * (right - left)
        y = bottom - value / 10 * (bottom - top)
        grid.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}"/><text x="{x:.1f}" y="350" text-anchor="middle">{value}</text>')
        grid.append(f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}"/><text x="58" y="{y + 4:.1f}" text-anchor="end">{value}</text>')
    marks = []
    legend = []
    colors = ["#075a9f", "#f5b400", "#279b7d", "#e2605f"]
    for index, (x_value, y_value, size) in enumerate(zip(x_values, y_values, bubble_sizes)):
        px = left + x_value / 10 * (right - left)
        py = bottom - y_value / 10 * (bottom - top)
        radius = 13 + math.sqrt(size / max_size) * 28
        label, label_en = labels_zh[index], labels_en[index]
        marks.append(
            f'<g class="bubblePoint" tabindex="0" data-chart-key="{esc(label_en)}">'
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{radius:.1f}" fill="{colors[index % len(colors)]}"/>'
            f'<text x="{px:.1f}" y="{py - 2:.1f}" text-anchor="middle" class="pointName" data-en="{esc(label_en)}">{esc(label)}</text>'
            f'<text x="{px:.1f}" y="{py + 13:.1f}" text-anchor="middle" class="pointValue">{size:g}</text>'
            f'<title>{esc(label_en)}: capability {x_value:g}, attractiveness {y_value:g}, capacity {size:g}</title></g>'
        )
        legend.append(f'<span><i style="background:{colors[index % len(colors)]}"></i><b data-en="{esc(label_en)}">{esc(label)}</b><small>能力 {x_value:g} / 吸引力 {y_value:g} / 容量 {size:g}</small></span>')
    return (
        f'<div class="insightScatter insightBubble" data-chart-id="{esc(chart_id)}"><header>'
        '<h4 data-en="Business opportunity matrix">业务机会矩阵</h4>'
        '<p data-en="Horizontal axis is organizational capability, vertical axis is market attractiveness, and bubble area represents the source market-capacity value.">横轴表示企业能力，纵轴表示市场吸引力，气泡面积表示资料中的市场容量。</p></header>'
        f'<svg viewBox="0 0 760 365" role="img" aria-label="起重机业务机会气泡图"><g class="scatterGrid">{"".join(grid)}</g>'
        f'<line class="scatterAxis" x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}"/><line class="scatterAxis" x1="{left}" y1="{top}" x2="{left}" y2="{bottom}"/>'
        '<text class="axisTitle" x="395" y="362" text-anchor="middle" data-en="Capability (0-10)">能力（0-10）</text>'
        '<text class="axisTitle" transform="translate(17 180) rotate(-90)" text-anchor="middle" data-en="Market attractiveness (0-10)">市场吸引力（0-10）</text>'
        f'{"".join(marks)}</svg><div class="scatterLegend">{"".join(legend)}</div></div>'
    )


def _render_chart(chart: dict[str, Any], slide_number: int, index: int) -> str:
    chart_id = f"slide-{slide_number}-chart-{index}"
    chart_type = chart.get("chart_type", "").upper()
    if "PIE" in chart_type or "DOUGHNUT" in chart_type:
        return _render_pie(chart, chart_id)
    if "BUBBLE" in chart_type:
        return _render_bubble(chart, chart_id)
    if "XY_SCATTER" in chart_type:
        return _render_scatter(chart, chart_id, slide_number)
    series = chart.get("series") or []
    if not chart.get("categories") and len(series) >= 2:
        return _render_scalar_comparison(chart, chart_id)
    return _render_columns(chart, chart_id)


def _render_regional_crane_sales(charts: list[dict[str, Any]]) -> str:
    """Render slide 7's four US/Canada charts as one comparable matrix."""
    labels = {
        "chart-05": ("通用底盘起重机", "Boom Trucks"),
        "chart-12": ("越野轮胎起重机", "Rough-Terrain Cranes"),
        "chart-08": ("全地面起重机", "All-Terrain Cranes"),
        "chart-09": ("履带起重机", "Crawler Cranes"),
    }
    ordered_ids = ("chart-05", "chart-12", "chart-08", "chart-09")
    by_id = {
        chart.get("id"): (index, chart)
        for index, chart in enumerate(charts, 1)
    }
    rows = []
    for chart_id in ordered_ids:
        chart_entry = by_id.get(chart_id)
        if not chart_entry:
            continue
        chart_index, chart = chart_entry
        categories = chart.get("categories") or []
        series = chart.get("series") or []
        values = series[0].get("values", []) if series else []
        if len(categories) < 2 or len(values) < 2:
            continue
        usa = float(values[0] or 0)
        canada = float(values[1] or 0)
        rows.append((labels[chart_id][0], labels[chart_id][1], usa, canada, chart_index))
    if not rows:
        return ""

    scale = max(max(usa, canada) for _zh, _en, usa, canada, _index in rows) or 1
    total_usa = sum(row[2] for row in rows)
    total_canada = sum(row[3] for row in rows)
    grand_total = total_usa + total_canada
    usa_share = total_usa / grand_total * 100 if grand_total else 0
    canada_share = total_canada / grand_total * 100 if grand_total else 0
    rendered_rows = []
    for label_zh, label_en, usa, canada, chart_index in rows:
        total = usa + canada
        rendered_rows.append(
            f'<div class="regionalSalesRow" role="row" data-chart-id="slide-7-chart-{chart_index}">'
            f'<b role="rowheader" data-en="{esc(label_en)}">{esc(label_zh)}</b>'
            '<div class="regionalSalesValue usa" role="cell">'
            f'<span><i style="width:{usa / scale * 100:.2f}%"></i></span><strong>{usa:,.0f}</strong></div>'
            '<div class="regionalSalesValue canada" role="cell">'
            f'<span><i style="width:{canada / scale * 100:.2f}%"></i></span><strong>{canada:,.0f}</strong></div>'
            f'<strong class="regionalSalesTotal" role="cell">{total:,.0f}</strong>'
            '</div>'
        )
    return (
        '<section class="regionalSalesMatrix" aria-label="2024年北美起重机销量区域分布" '
        'data-aria-label-en="2024 North American crane sales by country">'
        '<header><div><h4 data-en="2024 North American Crane Sales by Country">'
        '2024年北美起重机销量区域分布</h4>'
        '<p data-en="The four crane categories use one common scale; values are units.">'
        '四类起重设备使用同一比例尺，单位为台。</p></div>'
        '<div class="regionalSalesSummary">'
        f'<span><b>{grand_total:,.0f}</b><small data-en="units in chart scope">图表口径合计</small></span>'
        f'<span><b>{usa_share:.1f}%</b><small data-en="United States">美国</small></span>'
        f'<span><b>{canada_share:.1f}%</b><small data-en="Canada">加拿大</small></span>'
        '</div></header>'
        '<div class="regionalSalesTable" role="table">'
        '<div class="regionalSalesHead" role="row">'
        '<span data-en="Crane category">设备类别</span><span data-en="United States">美国</span>'
        '<span data-en="Canada">加拿大</span><span data-en="Total">合计</span></div>'
        f'{"".join(rendered_rows)}</div>'
        '<footer data-en="The chart records 2,380 units in the United States and 198 in Canada. Rough-terrain cranes are the largest of the four categories; Canada represents 7.7% of the chart total.">'
        f'图表记录美国 {total_usa:,.0f} 台、加拿大 {total_canada:,.0f} 台；越野轮胎起重机为四类中销量最高，加拿大占图表口径 {canada_share:.1f}%。'
        '</footer></section>'
    )


def _render_images(
    record: dict[str, Any],
    compact_captions: bool = False,
    seen_images: set[str] | None = None,
) -> str:
    images = list(record.get("images") or [])
    if seen_images is not None:
        images = [path for path in images if path not in seen_images]
        seen_images.update(images)
    if not images:
        return ""
    override_captions = IMAGE_CAPTION_OVERRIDES.get(record["slide"], ())
    override_captions_en = IMAGE_CAPTION_OVERRIDES_EN.get(record["slide"], ())
    figures: list[tuple[str, str]] = []
    for index, path in enumerate(images):
        ownership = IMAGE_OWNERSHIP_MAP.get(path)
        display_path = IMAGE_DISPLAY_MAP.get(path, path)
        preferred_path, preferred_size, asset_mode = _preferred_image_asset(path)
        thumbnail_path = THUMBNAIL_MAP.get(path, preferred_path)
        source_width, source_height = _source_image_size(path)
        display_width_px, display_height_px = _display_image_size(path)
        preferred_width_px, preferred_height_px = preferred_size
        quality_class = _source_quality_class(path)
        layout_class = _image_layout_class(path)
        aspect_group = _image_aspect_group(path)
        if index < len(override_captions):
            caption = override_captions[index]
            caption_en = (
                override_captions_en[index]
                if index < len(override_captions_en)
                else _en(caption)
            )
        else:
            base_caption = _display_title(record)
            base_caption_en = SLIDE_TITLE_OVERRIDES_EN.get(record["slide"], _en(base_caption))
            if compact_captions:
                if len(images) == 1:
                    caption = "现场影像"
                    caption_en = "Field image"
                elif "客户使用评价" in base_caption:
                    caption = f"评价细节 {index + 1}"
                    caption_en = f"Evaluation detail {index + 1}"
                elif "市场与工况" in base_caption:
                    caption = f"应用场景 {index + 1}"
                    caption_en = f"Application scene {index + 1}"
                else:
                    caption = f"图像 {index + 1}"
                    caption_en = f"Image {index + 1}"
            elif len(images) == 1:
                caption = base_caption
                caption_en = base_caption_en
            elif "客户使用评价" in base_caption:
                caption = f"{base_caption} · 评价图像 {index + 1}"
                caption_en = f"{base_caption_en} · Evaluation image {index + 1}"
            elif "市场与工况" in base_caption:
                caption = f"{base_caption} · 应用场景 {index + 1}"
                caption_en = f"{base_caption_en} · Application scene {index + 1}"
            else:
                caption = f"{base_caption} · 图像 {index + 1}"
                caption_en = f"{base_caption_en} · Image {index + 1}"
        current_slide = int(record["slide"])
        other_slides: list[int] = []
        if ownership and ownership.get("decision") == "SOURCE_REUSE":
            other_slides = sorted(
                int(value)
                for value in ownership.get("source_slides", [])
                if int(value) != current_slide
            )
        reused_slides = ",".join(str(value) for value in other_slides)
        display_width = _evidence_display_width(path)
        ratio_css = f"{preferred_width_px}/{preferred_height_px}" if preferred_width_px and preferred_height_px else "4/3"
        low_resolution = max(source_width, source_height) < 400
        quality_note_zh = (
            f"原始素材分辨率有限（{source_width}×{source_height}）"
            if low_resolution
            else ""
        )
        quality_note_en = (
            f"Original source resolution is limited ({source_width}×{source_height})"
            if low_resolution
            else ""
        )
        figures.append((
            aspect_group,
            f'<figure class="{quality_class} {layout_class} source-aspect-{aspect_group}" data-source-resolution="{source_width}x{source_height}" '
            f'data-image-source-slide="{current_slide}" data-image-reused-slides="{reused_slides}" '
            f'data-display-resolution="{display_width_px}x{display_height_px}" '
            f'data-render-resolution="{preferred_width_px}x{preferred_height_px}" data-asset-mode="{asset_mode}" '
            f'style="--evidence-max-width:{display_width}px;--evidence-ratio:{ratio_css}">'
            '<button type="button" class="insightImageButton" '
            f'data-full="{esc(path)}" data-full-src="{esc(path)}" data-source-src="{esc(path)}" data-ppt-src="{esc(display_path)}" '
            f'data-caption="{esc(caption_en)}" data-caption-zh="{esc(caption)}" data-caption-en="{esc(caption_en)}" '
            f'data-quality-note-zh="{esc(quality_note_zh)}" data-quality-note-en="{esc(quality_note_en)}" '
            f'aria-label="放大查看：{esc(caption)}" data-aria-label-en="Open full-size image: {esc(caption_en)}" '
            f'title="放大查看" data-title-en="Open full-size image">'
            f'<img src="{esc(thumbnail_path)}" alt="{esc(caption)}" data-alt-en="{esc(caption_en)}" '
            f'width="{preferred_width_px}" height="{preferred_height_px}" loading="lazy" decoding="async">'
            f'</button><figcaption data-en="{esc(caption_en)}">{esc(caption)}</figcaption></figure>'
        ))
    grouped: dict[str, list[str]] = {}
    for aspect_group, figure in figures:
        grouped.setdefault(aspect_group, []).append(figure)
    galleries = "".join(
        f'<div class="craneInsightGallery aspect-{aspect_group} count-{len(group)}" '
        f'data-aspect-group="{aspect_group}">{"".join(group)}</div>'
        for aspect_group, group in grouped.items()
    )
    return f'<div class="craneInsightGalleryGroups">{galleries}</div>'


def _render_class_visual_summary(records: list[dict[str, Any]]) -> str:
    groups = []
    for record in records:
        if not record.get("images"):
            continue
        title = _display_title(record)
        title_en = SLIDE_TITLE_OVERRIDES_EN.get(record["slide"], _en(title))
        source_long_edge = max(
            (max(_preferred_image_asset(path)[1]) for path in record["images"]),
            default=0,
        )
        if len(record["images"]) > 1:
            layout_class = "visual-multi"
        elif source_long_edge >= 900:
            layout_class = "visual-single-wide"
        else:
            layout_class = "visual-single-compact"
        groups.append(
            f'<article class="classVisualGroup {layout_class}" data-source-slide="{record["slide"]}">'
            f'<header><h4 data-en="{esc(title_en)}">{esc(title)}</h4>'
            f'<span data-en="{len(record["images"])} images">{len(record["images"])} 张</span></header>'
            f'{_render_images(record, compact_captions=True)}</article>'
        )
    if not groups:
        return ""
    return (
        '<section id="class-visuals" class="classVisualSummary"><div class="classVisualSummaryHead">'
        '<div><h3 data-en="Field Applications and Product Detail Images">现场应用与产品细节影像</h3>'
        '<p data-en="Regional applications, operating scenes, safety details and service observations are shown at full available resolution. Select any image to inspect it at larger scale.">'
        '集中展示区域应用、施工现场、安全细节与维修观察；点击任一图片可放大查看完整画面。</p></div>'
        f'<b data-en="{sum(len(record.get("images") or []) for record in records)} images">'
        f'{sum(len(record.get("images") or []) for record in records)} 张影像</b></div>'
        f'<div class="classVisualGroups">{"".join(groups)}</div></section>'
    )


def render_slide_record(
    record: dict[str, Any],
    include_media: bool = True,
    compact_context: bool = False,
    seen_images: set[str] | None = None,
) -> str:
    tables = [
        (index, table)
        for index, table in enumerate(record.get("tables", []), 1)
        if _meaningful_table(table)
    ]
    if record["slide"] == 7:
        charts = [_render_regional_crane_sales(record.get("charts", []))]
    else:
        charts = [
            _render_chart(chart, record["slide"], index)
            for index, chart in enumerate(record.get("charts", []), 1)
        ]
    charts = [chart for chart in charts if chart]
    body = _paragraphs(record)
    media = _render_images(record, seen_images=seen_images) if include_media else ""
    table_html = "".join(
        _render_table(table, record["slide"], index)
        for index, table in tables
    )
    visual_html = "".join(charts)
    content_class = " has-media" if media else ""
    if len(record.get("images") or []) >= 3:
        content_class += " many-media"
    record_label = SECTION_LABELS.get(record.get("section"), "产品分析")
    record_label_en = SECTION_LABELS_EN.get(record.get("section"), "Product Analysis")
    title = _display_title(record)
    title_en = SLIDE_TITLE_OVERRIDES_EN.get(record["slide"], _en(title))
    label_html = "" if compact_context else (
        f'<span class="recordLabel" data-en="{esc(record_label_en)}">{esc(record_label)}</span>'
    )
    status_html = (
        _status_badge(record["status"])
        if not compact_context or record["status"] == "plan"
        else ""
    )
    footer_html = "" if compact_context else (
        f'<footer data-en="Source date {SOURCE_DATE} · Record CR-{record["slide"]:03d}">'
        f'资料日期 {SOURCE_DATE} · 记录号 CR-{record["slide"]:03d}</footer>'
    )
    context_class = " contextRecord" if compact_context else ""
    return (
        f'<article class="craneInsightRecord{content_class}{context_class}" data-source-slide="{record["slide"]}" '
        f'data-source-status="{esc(record["status"])}">'
        '<header><div>'
        f'{label_html}<h3 data-en="{esc(title_en)}">{esc(title)}</h3></div>{status_html}</header>'
        f'<div class="recordBody"><div class="recordNarrative">{body}</div>{media}</div>'
        f'{visual_html}{table_html}'
        f'{footer_html}'
        '</article>'
    )


def render_source_register(slide_numbers: Iterable[int]) -> str:
    numbers = sorted(set(int(number) for number in slide_numbers))
    if not numbers:
        return ""
    ranges = []
    start = previous = numbers[0]
    for number in numbers[1:]:
        if number == previous + 1:
            previous = number
            continue
        ranges.append(f"{start}" if start == previous else f"{start}-{previous}")
        start = previous = number
    ranges.append(f"{start}" if start == previous else f"{start}-{previous}")
    return (
        '<div class="craneSourceRegister"><b data-en="Source scope">资料范围</b>'
        f'<span>CR-{esc(", CR-".join(ranges))}</span>'
        f'<small data-en="Source date: {SOURCE_DATE}; historical facts, source-date assessments and future plans are labelled separately.">'
        f'资料日期：{SOURCE_DATE}；历史事实、资料日期判断和未来规划已分开标识。</small></div>'
    )


def render_class_context(class_id: str, language: str = "zh") -> str:
    data = load_crane_insights()
    if class_id not in CLASS_SLIDES:
        raise KeyError(class_id)
    intro_zh, intro_en = CLASS_INTRO[class_id]
    segment = data["segments"][class_id]
    status = "plan" if segment["source_scope"] == "plan" else "current-at-source-date"
    sections = []
    shared_notice = ""
    if class_id in SHARED_RESEARCH_NOTICES:
        notice = SHARED_RESEARCH_NOTICES[class_id]
        shared_notice = (
            f'<aside class="sharedResearchNotice" data-shared-class="{esc(notice["shared_class"])}">'
            '<b data-en="Research boundary">资料边界</b>'
            f'<p data-en="{esc(notice["en"])}">{esc(notice["zh"])}</p>'
            '</aside>'
        )
    seen_images: set[str] = set()
    for section_id, title_zh, title_en, lead_zh, lead_en in CLASS_PAGE_SECTIONS:
        if section_id == "market-insight":
            lead_zh = f"{intro_zh}{lead_zh}"
            lead_en = f"{intro_en} {lead_en}"
        slide_numbers = CLASS_SECTION_SLIDES[class_id][section_id]
        records = [data["by_slide"][number] for number in slide_numbers]
        if records:
            records_html = "".join(
                render_slide_record(
                    record,
                    include_media=True,
                    compact_context=True,
                    seen_images=seen_images,
                )
                for record in records
            )
        else:
            records_html = (
                '<div class="classEvidenceBoundary"><b data-en="No class-specific field evidence is available">'
                '当前缺少该吨级专属现场证据</b>'
                '<p data-en="The available source does not provide verified jobsite images, customer evaluation or machine-test results for this class. No conclusions are inferred from adjacent classes.">'
                '现有资料未提供该吨级可核验的施工影像、客户评价或实机测试结果；页面不引用相邻吨级结论代替。</p></div>'
            )
        badge = (
            _status_badge(status)
            if status == "plan" and section_id == "product-positioning"
            else ""
        )
        sections.append(
            f'<section id="{esc(section_id)}" class="craneInsightSection classContextGroup {esc(section_id)}">'
            '<div class="insightSectionHead"><div>'
            f'<h2 data-en="{esc(title_en)}">{esc(title_zh)}</h2>'
            f'<p data-en="{esc(lead_en)}">{esc(lead_zh)}</p></div>{badge}</div>'
            f'<div class="craneInsightRecords">{records_html}</div></section>'
        )
    return shared_notice + "".join(sections)


def render_market_overview(language: str = "zh") -> str:
    data = load_crane_insights()
    sections = []
    all_numbers = []
    for section_id, title_zh, title_en, lead_zh, lead_en, numbers in REPORT_SECTIONS:
        records = [data["by_slide"][number] for number in numbers if number != 1]
        all_numbers.extend(numbers)
        source_attributes = ' data-source-slide="1" data-source-status="current-at-source-date"' if 1 in numbers else ""
        sections.append(
            f'<section id="{esc(section_id)}" class="craneInsightSection reportBand"{source_attributes}>'
            '<div class="insightSectionHead"><div>'
            f'<h2 data-en="{esc(title_en)}">{esc(title_zh)}</h2>'
            f'<p data-en="{esc(lead_en)}">{esc(lead_zh)}</p></div>'
            f'<span class="sectionCount" data-en="{len(numbers)} analyses">{len(numbers)} 项分析</span></div>'
            f'<div class="craneInsightRecords">{"".join(render_slide_record(record) for record in records)}</div>'
            '</section>'
        )
    return "".join(sections) + render_source_register(all_numbers)


def report_navigation() -> str:
    links = "".join(
        f'<a href="#{esc(section_id)}" data-en="{esc(title_en)}">{esc(title_zh)}</a>'
        for section_id, title_zh, title_en, _lead_zh, _lead_en, _numbers in REPORT_SECTIONS
    )
    return (
        '<a class="home" href="arc.html" data-en="Return to Platform Home">返回对标平台主页</a>'
        + links
    )


def render_site_credits() -> str:
    return '''<div class="siteCredits" aria-label="项目署名">
  <span data-en="Executive Sponsor: Zhang Shengnan">指导领导：张盛楠</span>
  <span data-en="Data Visualization: Liu Chang">数据可视化：刘畅</span>
  <span data-en="Data Source: ARC Product Team">数据来源：ARC产品小组</span>
  <span><span data-en="Issue Reporting:">问题提报：</span> <a href="mailto:changl@xcmgarc.com">changl@xcmgarc.com</a></span>
</div>'''


def render_market_report_page(asset_version: str) -> str:
    return f'''<!doctype html>
<html lang="zh-CN" data-language="zh"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title data-en="North American Crane Market and Product Insight | XCMG ARC">北美起重机市场与产品洞察 | XCMG ARC</title>
<link rel="stylesheet" href="assets/dashboard.css?v={asset_version}">
<link rel="stylesheet" href="assets/site-credits.css?v=20260724a">
<link rel="stylesheet" href="assets/crane-dashboard.css?v=20260812d">
<link rel="stylesheet" href="assets/crane-insights.css?v=20260812g">
</head><body>
<a class="backTop" href="#top" aria-label="回到页面顶部" data-en="Back to top">回到顶部</a>
<div class="layout" id="top"><aside class="nav">
<a class="navBrand" href="arc.html"><img src="assets/xcmg-logo.svg" alt="XCMG"></a>
<div><div class="navTitle" data-en="North American Crane Insight">北美起重机市场洞察</div><small>XCMG ARC</small></div>
<button class="languageToggle" type="button">EN</button>
<button class="sidebarToggle" type="button"><span data-en="Collapse navigation">收起侧栏</span></button>
<button class="navToggle" type="button" data-en="Page navigation">页面导航</button>
<div class="navMenu" id="page-nav">{report_navigation()}</div></aside><main>
<header class="hero craneReportHero"><div class="heroText"><p class="eyebrow">CRANE MARKET AND PRODUCT INTELLIGENCE</p>
<h1 data-en="North American Crane Market and Product Insight">北美起重机市场与产品洞察</h1>
<p data-en="A complete view of market structure, regional demand, customer applications, product evaluation, portfolio gaps, roadmap, channels, service and localization.">覆盖市场结构、区域需求、客户工况、产品评价、型谱空白、产品路线图、渠道、服务和本地化保供，形成从市场到产品决策的完整分析。</p>
<div class="reportKpis"><span><b>163</b><small data-en="analysis records">项分析记录</small></span><span><b>4</b><small data-en="crane classes">类起重设备</small></span><span><b>9</b><small data-en="North American regions">个北美区域</small></span><span><b>2025-07</b><small data-en="source date">资料日期</small></span></div>
</div><figure class="heroMedia craneHeroMedia"><img src="assets/arc/category-cranes.webp" alt="XCMG crane product line"><figcaption data-en="XCMG crane product line">XCMG 起重设备产品线</figcaption></figure></header>
<section class="reportScope"><b data-en="Market, regional, product and service insight">市场、区域、产品与服务洞察</b><p data-en="The market report presents information that cuts across capacity classes. Rough-terrain and all-terrain classes with governed Excel datasets retain their specifications, equipment, work-condition and ranking analyses on the corresponding benchmark pages.">总体报告承载跨吨级信息；已有Excel数据的越野吊与全地面吨级继续在各自正式页面中展示参数、配置、工况和排名。</p></section>
{render_market_overview()}
{render_site_credits()}
</main></div><script src="assets/dashboard.js?v={asset_version}"></script><script src="assets/i18n.js?v=20260805e"></script><script src="assets/crane-insights.js?v=20260812g"></script>
</body></html>'''


def render_legacy_redirect() -> str:
    return '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="0;url=crane-market-overview.html">
<title>正在进入北美起重机市场洞察 | XCMG ARC</title></head><body>
<p><a href="crane-market-overview.html">进入北美起重机市场洞察</a></p>
<script>location.replace("crane-market-overview.html" + location.search + location.hash);</script>
</body></html>'''
