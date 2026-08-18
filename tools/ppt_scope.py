"""Authoritative PPT-to-dashboard scope rules.

Keep slide ownership in one place so narrative, tables, translations and tests
cannot silently drift apart. Shared source chapters are mapped to both product
pages; class-specific sales and comparison slides remain exclusive.
"""

from __future__ import annotations


OVERVIEW_SLIDES = (
    *range(3, 19),
    *range(236, 246),
    247,
)


SLUG_SLIDE_RANGES = {
    "excavator-1-2t": ((19, 37),),
    "excavator-2-3t": ((38, 50),),
    "excavator-35t": ((51, 71),),
    "excavator-4-5t": ((72, 92),),
    "excavator-5-6t": ((93, 110),),
    "excavator-8-10t": ((111, 128),),
    # Slides 128-136 and 145-151 explicitly cover the combined 12-16 t
    # class. Sales and comparison pages for the individual classes remain
    # exclusive to the matching dashboard.
    "excavator-12-14t": ((129, 129), (131, 143), (148, 154)),
    "excavator-14-16t-short-tail": ((130, 139), (144, 154)),
    "excavator-21-24t": ((155, 171),),
    # Slides 171-176 are shared 24-33 t application analysis. Slide 169 and
    # 177-187 are 24-28 t only; slide 170 and 188-198 are 28-33 t only.
    "excavator-24-28t": ((172, 172), (174, 190)),
    "excavator-24-28t-short-tail": ((172, 172), (174, 190)),
    "excavator-28-33t": ((173, 179), (191, 201)),
    "excavator-33-40t": ((202, 218),),
    "excavator-40-60t": ((219, 235),),
}


# Slide 115's source heading says 5-6 t, while its table, XE80U/KX080-5
# models, application text and surrounding chapter all identify 8-10 t.
# Keep the raw source heading in extracted records, but use this corrected
# display heading to prevent a contradictory reader-facing section.
DISPLAY_TITLE_OVERRIDES = {}


SLUG_ALLOWED_TONNAGE_LABELS = {
    "excavator-1-2t": {"1-2"},
    "excavator-2-3t": {"2-3"},
    "excavator-35t": {"3-4"},
    "excavator-4-5t": {"4-5"},
    "excavator-5-6t": {"5-6"},
    "excavator-8-10t": {"8-10"},
    "excavator-12-14t": {"12-14", "12-16"},
    "excavator-14-16t-short-tail": {"14-16", "12-16"},
    "excavator-21-24t": {"19-24"},
    "excavator-24-28t": {"24-28", "24-33"},
    "excavator-24-28t-short-tail": {"24-28", "24-33"},
    "excavator-28-33t": {"28-33", "24-33"},
    "excavator-33-40t": {"33-40"},
    "excavator-40-60t": {"40-60"},
}


def slugs_for_slide(slide_number: int) -> list[str]:
    return [
        slug
        for slug, ranges in SLUG_SLIDE_RANGES.items()
        if any(start <= slide_number <= end for start, end in ranges)
    ]


def display_title(slide_number: int, source_title: str) -> str:
    return DISPLAY_TITLE_OVERRIDES.get(slide_number, source_title)
