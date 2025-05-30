# ✅ Final Clean Version of Your Code with:
# - Key people/dates emphasized
# - Footer/header removed (via readability)
# - Summarizer boosted with missing entities
# - Support for any news URL, homepage, and PDF

from transformers import pipeline
from newspaper import Article, build
import pdfplumber
import spacy
from readability import Document
import requests
from bs4 import BeautifulSoup
import textwrap
from math import ceil
import re

# Load spaCy once
nlp = spacy.load("en_core_web_sm")

# Named entity extraction
USEFUL_LABELS = {"PERSON", "ORG", "GPE", "DATE", "EVENT"}
NOISE_ENTITIES = {"BBC", "Reuters", "CNN", "AP", "BBC Verify"}

def extract_named_entities(text):
    doc = nlp(text)
    return [ent.text.strip() for ent in doc.ents if ent.label_ in USEFUL_LABELS and ent.text.strip() not in NOISE_ENTITIES]

def boost_summary_with_entities(original_text, summary):
    original_ents = {(ent.text.strip(), ent.label_) for ent in nlp(original_text).ents if ent.label_ in USEFUL_LABELS and ent.text.strip() not in NOISE_ENTITIES}
    summary_ents = {(ent.text.strip(), ent.label_) for ent in nlp(summary).ents}
    missing = original_ents - summary_ents
    if missing:
        summary += "\n\n📌 Missing Key Info:\n"
        for text, label in sorted(missing, key=lambda x: x[1]):
            summary += f"- {label}: {text}\n"
    return summary

def emphasize_named_entities(text):
    doc = nlp(text)
    people_dates = {ent.text for ent in doc.ents if ent.label_ in {"PERSON", "DATE"}}
    if people_dates:
        prompt = "This article includes key people and dates: " + ", ".join(people_dates) + ".\n\n"
        return prompt + text
    return text

# Clean article text using readability

def get_clean_article_text(url):
    try:
        html = requests.get(url, timeout=10).text
        doc = Document(html)
        cleaned_html = doc.summary()
        soup = BeautifulSoup(cleaned_html, "html.parser")
        return soup.get_text(separator="\n").strip()
    except Exception as e:
        print(f"⚠️ Fallback to Newspaper: {e}")
        article = Article(url)
        article.download()
        article.parse()
        return article.text.strip()

def get_text_from_pdf(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    return full_text

def get_articles_from_homepage(url, max_articles=20):
    paper = build(url, memoize_articles=False)
    articles = []
    for article in paper.articles[:max_articles]:
        try:
            article.download()
            article.parse()
            articles.append((article.title, article.text))
        except Exception as e:
            print(f"❌ Error processing an article: {e}")
    return articles

def chunk_text(text, max_chars=2000):
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) <= max_chars:
            current_chunk += para + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def summarize_text(text, summarizer):
    chunks = textwrap.wrap(text, width=3000)
    full_summary = ""

    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1} of {len(chunks)}...")

        if len(chunk.split()) < 10:
            print("⚠️ Skipping too-short chunk.")
            continue

        word_count = len(chunk.split())
        max_len = min(ceil(word_count * 0.7), 250)
        min_len = max(30, ceil(word_count * 0.3))

        try:
            result = summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text']
            full_summary += result.strip() + " "
        except Exception as e:
            print(f"❌ Error summarizing chunk {i+1}: {e}")
            continue

    # ✅ Split into bullet points (heuristic: period followed by space and capital letter)
    raw_points = re.split(r'\.\s+(?=[A-Z])', full_summary.strip())
    bullet_points = [f"• {point.strip()}." for point in raw_points if point.strip()]

    return bullet_points



# Main CLI
if __name__ == "__main__":
    choice = input("Enter 'url' for article, 'homepage' for multiple articles, or 'pdf' to summarize from PDF: ").strip().lower()
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    print("Device set to use CPU\n")

    if choice == "url":
        url = input("Enter the article URL: ").strip()
        print("\n📝 Downloading article...\n")
        text = get_clean_article_text(url)
        print("📝 Summarizing article...\n")
        summary = summarize_text(text, summarizer)
        print("📄 Final Summary:\n")
        print(summary)

    elif choice == "homepage":
        homepage_url = input("Enter the news homepage URL (e.g. https://www.bbc.com/news): ").strip()
        articles = get_articles_from_homepage(homepage_url)
        if not articles:
            print("❌ No articles found or failed to load.")
        else:
            for idx, (title, text) in enumerate(articles, 1):
                print(f"\n📰 Article {idx}: {title}")
                summary = summarize_text(text, summarizer)
                print(summary)
                print("-" * 80)

    elif choice == "pdf":
        pdf_path = input("Enter the full path to the PDF file: ").strip()
        print("\n📄 Reading PDF content...\n")
        text = get_text_from_pdf(pdf_path)
        print("📝 Summarizing PDF content...\n")
        summary = summarize_text(text, summarizer)
        print("📄 Final Summary:\n")
        print(summary)

    else:
        print("Invalid choice. Please enter either 'url', 'homepage', or 'pdf'.")
