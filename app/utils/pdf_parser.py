# app/utils/pdf_parser.py
import io
import pdfplumber

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with io.BytesIO(file_bytes) as fh:
        try:
            with pdfplumber.open(fh) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            # fallback: try to decode bytes
            try:
                text = file_bytes.decode('utf-8', errors='ignore')
            except:
                text = ""
    return text
