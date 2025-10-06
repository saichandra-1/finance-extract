# app/models/bert_model.py
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import os

# Default small NER model - replace this with your fine-tuned FinBERT checkpoint if you have one.
# Note: Using bigger models may require more RAM/GPUs on Render.
MODEL_NAME = os.getenv("BERT_MODEL_NAME", "dslim/bert-base-NER")

# initialize on import (slow at first run)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)

nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

def extract_entities_bert(text: str):
    """
    Returns list of {'entity': 'ORG'/'PER'/..., 'word': '...', 'score': 0.99, 'start':int, 'end':int}
    """
    result = nlp(text)
    # Ensure serializable
    out = []
    for ent in result:
        out.append({
            "entity": ent.get("entity_group", ent.get("entity")),
            "word": ent.get("word"),
            "score": float(ent.get("score", 0)),
            "start": ent.get("start"),
            "end": ent.get("end"),
        })
    return out
