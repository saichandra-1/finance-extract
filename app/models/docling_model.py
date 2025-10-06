# app/models/docling_model.py
# Docling is an optional external library. This wrapper tries to import and uses a fallback if not installed.
def extract_entities_docling(text: str):
    try:
        import docling
        # Pseudocode: replace with your docling usage (depends on docling API)
        extractor = docling.Docling()  # example only
        return extractor.extract(text)
    except Exception as e:
        # fallback: return empty or stick with regex results
        return {"docling_available": False, "note": "docling not installed; fallback used"}
