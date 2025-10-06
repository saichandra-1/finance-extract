# app/models/regex_model.py
import re

# Patterns
CURRENCY_PATTERN = re.compile(r'(\$|USD|EUR|GBP|INR|Rs\.?)\s?[\d{1,3},]+(?:\.\d+)?(?:\s?(?:million|billion|bn|mn|k|m|crore))?', re.IGNORECASE)
NUMBER_PATTERN = re.compile(r'\b\d{1,3}(?:[,\d{3}])*(?:\.\d+)?\b')
PHONE_PATTERN = re.compile(r'(\+?\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?\d{6,12}')
TICKER_PATTERN = re.compile(r'\b[A-Z]{2,5}\b')  # naive: uppercase tickers

def extract_entities_regex(text: str):
    out = {"monetary": [], "numbers": [], "phones": [], "tickers": []}
    for m in CURRENCY_PATTERN.finditer(text):
        context_start = max(0, m.start() - 40)
        context_end = min(len(text), m.end() + 40)
        context = text[context_start:context_end]
        out["monetary"].append({"match": m.group(0), "start": m.start(), "end": m.end(), "context": context})

    for m in PHONE_PATTERN.finditer(text):
        out["phones"].append({"match": m.group(0), "start": m.start(), "end": m.end()})

    # numbers (may be ratios, percents, etc.)
    for m in NUMBER_PATTERN.finditer(text):
        out["numbers"].append({"match": m.group(0), "start": m.start(), "end": m.end()})

    # naive ticker extraction: look for UPPERCASE words with short length nearby "share", "close"
    for m in TICKER_PATTERN.finditer(text):
        out["tickers"].append({"match": m.group(0), "start": m.start(), "end": m.end()})

    return out
