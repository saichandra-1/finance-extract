# app/models/spacy_model.py
import spacy
from spacy import util
import os

# Use small model for portability. You can switch to a larger/more accurate model.
SPACY_MODEL = os.getenv("SPACY_MODEL", "en_core_web_sm")

# ensure model is available under Dockerfile we will download it
nlp = spacy.load(SPACY_MODEL)

def extract_entities_spacy(text: str):
    doc = nlp(text)
    out = []
    for ent in doc.ents:
        out.append({"label": ent.label_, "text": ent.text, "start": ent.start_char, "end": ent.end_char})
    return out
