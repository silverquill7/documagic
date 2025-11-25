import io, os
import pdfplumber
from PIL import Image
import pytesseract

def extract_text_from_pdf(path: str) -> str:
    text_parts = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                txt = page.extract_text() or ""
                text_parts.append(txt)
    except Exception as e:
        # fall back to OCR if pdfplumber fails
        text_parts.append(ocr_pdf(path))
    return "\n".join(text_parts)

def ocr_pdf(path: str) -> str:
    # convert each page to image via pdfplumber and OCR using pytesseract
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pil_image = page.to_image(resolution=200).original
            text = pytesseract.image_to_string(pil_image)
            text_parts.append(text)
    return "\n".join(text_parts)

def extract_basic_fields(text: str) -> dict:
    # VERY simple rule-based extraction. Replace/extend with ML later.
    parsed = {}
    import re
    # Example: invoice number
    m = re.search(r'(invoice\s*no\.?|inv#|invoice number)[:\s]*([A-Z0-9-]+)', text, re.I)
    if m:
        parsed['invoice_number'] = m.group(2).strip()
    # Amount
    m2 = re.search(r'([₹$€]\s*\d[\d,\.]*)', text)
    if m2:
        parsed['amount'] = m2.group(1).strip()
    # Date
    m3 = re.search(r'\b(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})\b', text)
    if m3:
        parsed['date'] = m3.group(1)
    return parsed
