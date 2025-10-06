# app/utils/entity_formatter.py
from typing import Dict, List
import re

# Map user-facing selection names to keys we can find in outputs
SELECTION_MAP = {
    "Company Names": ["bert", "spacy"],  # ORG in BERT, ORG in spaCy
    "Stock Prices": ["regex"],
    "Revenue": ["regex"],
    "Market Cap": ["regex"],
    "Earnings": ["regex", "spacy"],
    "Financial Ratios": ["regex"],
    "Financial Dates": ["spacy"],
    "Financial Events": ["spacy", "docling"],
    "Phonenumber": ["regex"],
}

def filter_entities_by_selection(all_outputs: Dict, selections: List[str]):
    if not selections:
        return {}

    filtered = {}
    for sel in selections:
        keys = SELECTION_MAP.get(sel, [])
        hits = []
        for key in keys:
            src = all_outputs.get(key)
            if not src:
                continue
            # simple heuristics: include everything from that extractor for now
            hits.extend(src if isinstance(src, list) else [src])
        filtered[sel] = hits
    return filtered
