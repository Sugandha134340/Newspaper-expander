# pdf_extractor.py

import fitz  # PyMuPDF
import re

def extract_text_blocks_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    return full_text

def extract_headlines_and_paragraphs(pdf_text):
    # Split into lines and filter
    lines = [line.strip() for line in pdf_text.split('\n') if line.strip()]
    
    result = []
    current_headline = None
    current_paragraph = ""

    for line in lines:
        # A simple heuristic: Headlines are often ALL CAPS or Title Case and short
        if re.match(r'^([A-Z][A-Z\s]{3,}|[A-Z][a-z]+(\s[A-Z][a-z]+)+)$', line) and len(line.split()) <= 10:
            if current_headline and current_paragraph:
                result.append((current_headline, current_paragraph.strip()))
            current_headline = line
            current_paragraph = ""
        else:
            current_paragraph += " " + line

    # Add the last one
    if current_headline and current_paragraph:
        result.append((current_headline, current_paragraph.strip()))

    return result
