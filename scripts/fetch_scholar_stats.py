#!/usr/bin/env python3
"""Fetch Google Scholar stats, classify publications, extract venues → _data/stats.yml."""

import re
import sys
import yaml
from collections import Counter
from datetime import datetime

SCHOLAR_ID  = "Ss5594IAAAAJ"
OUTPUT_PATH = "_data/stats.yml"

# ── Publication type classification ───────────────────────────────────────────
# Checked in order; journal markers come first so "Proceedings of the ACM on …"
# (IMWUT = a journal) is not caught by the later "proceedings" conference rule.

JOURNAL_MARKERS = [
    "proceedings of the acm on interactive",  # IMWUT family
    "advances in building energy",
    "energy informatics",
    "computers, environment",
    "future generation computer systems",
    "international journal",
    "journal of",
    "journal on",
    "acm transactions",
    "ieee transactions",
    "transactions on",
    "softwarex",
    "energy and buildings",
    "scientific data",
    "social computing",
    "intelligent transportation systems research",
    "parallel and distributed computing",
    "sustainable energy",
]

CONFERENCE_MARKERS = [
    "conference", "workshop", "symposium",
    "proceedings",       # all remaining after journal check
    "general meeting", "summer study", "techfest",
    "annual meeting", "forum", "congress",
]

# ── Venue name mapping ─────────────────────────────────────────────────────────
# Each entry: (substring to match in citation.lower(), display name, pub_type)
# Listed longest/most-specific first to avoid partial matches.

VENUE_MAP = [
    # Journals
    ("proceedings of the acm on interactive",           "IMWUT (Proc. ACM)",                     "journals"),
    ("advances in building energy research",             "Advances in Building Energy Research",   "journals"),
    ("energy informatics",                               "Energy Informatics",                     "journals"),
    ("computers, environment and urban systems",         "Computers, Environment & Urban Systems", "journals"),
    ("future generation computer systems",               "Future Generation Computer Systems",     "journals"),
    ("international journal of intelligent transportation", "Int'l J. Intelligent Transportation", "journals"),
    ("journal of social computing",                      "Journal of Social Computing",            "journals"),
    ("scientific data",                                  "Scientific Data",                        "journals"),
    ("softwarex",                                        "SoftwareX",                              "journals"),
    ("energy and buildings",                             "Energy and Buildings",                   "journals"),
    # Conferences
    ("computing frontiers",                              "ACM Computing Frontiers",                "conferences"),
    ("american control conference",                      "American Control Conference (ACC)",      "conferences"),
    ("power & energy society general meeting",           "IEEE PES General Meeting",               "conferences"),
    ("power and energy society general meeting",         "IEEE PES General Meeting",               "conferences"),
    ("pervasive computing and communication",            "IEEE PerCom",                            "conferences"),
    ("high performance extreme computing",               "IEEE HPEC",                              "conferences"),
    ("systems for energy",                               "ACM BuildSys / e-Energy",                "conferences"),
    ("future energy systems",                            "ACM e-Energy",                           "conferences"),
    ("joint conference on pervasive",                    "ACM UbiComp",                            "conferences"),
    ("pervasive and ubiquitous computing",               "ACM UbiComp",                            "conferences"),
    # Others
    ("arxiv",                                            "arXiv Preprint",                         "others"),
    ("pacific northwest national laboratory",            "PNNL Technical Report",                  "others"),
    ("pnnl",                                             "PNNL Technical Report",                  "others"),
    ("iiit-delhi",                                       "Thesis",                                 "others"),
    ("iiit delhi",                                       "Thesis",                                 "others"),
    ("raytheon",                                         "Technical Report",                       "others"),
    ("urban freight lab",                                "Technical Report",                       "others"),
    ("us department of energy",                          "DOE Software",                           "others"),
    ("jacow",                                            "JACoW",                                  "others"),
    ("agu fall meeting",                                 "AGU Fall Meeting",                       "others"),
    ("smart cyber",                                      "Book Chapter",                           "others"),
]


def classify(pub: dict) -> str:
    c = (pub.get("bib", {}).get("citation") or "").lower()
    for m in JOURNAL_MARKERS:
        if m in c:
            return "journals"
    for m in CONFERENCE_MARKERS:
        if m in c:
            return "conferences"
    return "others"


def venue_of(pub: dict):
    """Return (display_name, pub_type) or None if unknown."""
    c = (pub.get("bib", {}).get("citation") or "").lower()
    if not c.strip():
        return None
    for pattern, name, ptype in VENUE_MAP:
        if pattern in c:
            return (name, ptype)
    return None


def main():
    try:
        from scholarly import scholarly
    except ImportError:
        print("scholarly not installed.  pip install scholarly pyyaml")
        sys.exit(1)

    print(f"Fetching Google Scholar profile: {SCHOLAR_ID}")
    try:
        author = scholarly.search_author_id(SCHOLAR_ID)
        author = scholarly.fill(author)
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    pubs = author.get("publications", [])

    # ── classify ──
    type_counts: Counter = Counter(classify(p) for p in pubs)

    # ── venues ──
    venue_counter: Counter = Counter()
    venue_type: dict[str, str] = {}
    for p in pubs:
        v = venue_of(p)
        if v:
            name, ptype = v
            venue_counter[name] += 1
            venue_type[name] = ptype

    venues_sorted = [
        {"name": name, "count": cnt, "type": venue_type[name]}
        for name, cnt in venue_counter.most_common()
    ]

    print("\nVenues:")
    for v in venues_sorted:
        print(f"  [{v['type']:12s}] {v['name']:50s} × {v['count']}")

    stats = {
        "publications":    len(pubs),
        "citations":       author.get("citedby"),
        "h_index":         author.get("hindex"),
        "i10_index":       author.get("i10index"),
        "pub_journals":    type_counts["journals"],
        "pub_conferences": type_counts["conferences"],
        "pub_others":      type_counts["others"],
        "pub_venues":      venues_sorted,
        "last_updated":    datetime.utcnow().strftime("%B %Y"),
    }

    with open(OUTPUT_PATH, "w") as f:
        f.write("# Auto-updated by .github/workflows/update-scholar-stats.yml\n")
        yaml.dump(stats, f, default_flow_style=False, allow_unicode=True)

    print(f"\nWritten to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
