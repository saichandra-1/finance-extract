# app/main.py
import os
from fastapi import FastAPI, File, UploadFile, Form, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from app.utils.pdf_parser import extract_text_from_pdf
from app.models.bert_model import extract_entities_bert
from app.models.spacy_model import extract_entities_spacy
from app.models.regex_model import extract_entities_regex
from app.models.docling_model import extract_entities_docling

API_KEY = os.getenv("API_KEY")  # set this in Render environment

app = FastAPI(title="FinanceInsight NER API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production to your frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/process/")
async def process_document(
    model: str = Form(...),
    entities: str = Form(""),  # comma-separated user selections
    file: UploadFile = File(...),
    x_api_key: str = Header(None),
):
    # API key check
    if API_KEY:
        if not x_api_key or x_api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API key")

    # Read file bytes
    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)
    if not text or text.strip() == "":
        return JSONResponse({"error": "No text found in PDF or empty PDF"}, status_code=400)

    # Run all extractors (we will return everything)
    outputs = {}
    # BERT NER
    try:
        outputs["bert"] = extract_entities_bert(text)
    except Exception as e:
        outputs["bert_error"] = str(e)

    # spaCy
    try:
        outputs["spacy"] = extract_entities_spacy(text)
    except Exception as e:
        outputs["spacy_error"] = str(e)

    # regex-based financial extractor
    try:
        outputs["regex"] = extract_entities_regex(text)
    except Exception as e:
        outputs["regex_error"] = str(e)

    # docling (optional)
    try:
        outputs["docling"] = extract_entities_docling(text)
    except Exception as e:
        outputs["docling_error"] = str(e)

    # Filter requested entities
    requested = [s.strip() for s in entities.split(",") if s.strip()]
    # entity_formatter will examine outputs and return filtered results
    from app.utils.entity_formatter import filter_entities_by_selection
    filtered = filter_entities_by_selection(outputs, requested)

    return {
        "metadata": {"model_requested": model, "requested_entities": requested},
        "all_outputs": outputs,
        "filtered_results": filtered,
    }
