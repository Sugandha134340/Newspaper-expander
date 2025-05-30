import streamlit as st
import os
from transformers import pipeline
from summarize_news import (
    get_clean_article_text,
    get_text_from_pdf,
    get_articles_from_homepage,
    summarize_text,
)
from pdf_extractor import extract_text_blocks_from_pdf, extract_headlines_and_paragraphs

st.set_page_config(page_title="News Summarizer", layout="centered")
st.title("📰 News Summarizer")
# Initialize summarizer once
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()



input_type = st.radio(
    "Choose input type:",
    options=["URL", "Homepage", "PDF"],
    index=0,
    horizontal=True,
)

# URL Article
if input_type == "URL":
    url = st.text_input("Enter article URL:")
    if url and st.button("Summarize Article"):
        with st.spinner("Fetching and summarizing article..."):
            try:
                text = get_clean_article_text(url)
                summary = summarize_text(text, summarizer)
                st.markdown("### 📝 Summary:")
                for bullet in summary:
                    st.markdown(bullet)
            except Exception as e:
                st.error(f"❌ Failed to summarize URL: {e}")

# Homepage with multiple articles
elif input_type == "Homepage":
    homepage_url = st.text_input("Enter homepage URL (e.g., https://www.bbc.com/news):")
    if homepage_url and st.button("Summarize Articles"):
        with st.spinner("Fetching and summarizing multiple articles..."):
            try:
                articles = get_articles_from_homepage(homepage_url)
                if not articles:
                    st.warning("⚠️ No articles found.")
                else:
                    for idx, (title, text) in enumerate(articles, 1):
                        summary = summarize_text(text, summarizer)
                        st.markdown(f"### 📰 Article {idx}: {title}")
                        for bullet in summary:
                            st.markdown(bullet)
                        st.markdown("---")
            except Exception as e:
                st.error(f"❌ Failed to summarize homepage: {e}")

# PDF Upload
elif input_type == "PDF":
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    
    pdf_mode = st.radio("Choose summarization mode:", ["Full Document", "By Headline/Paragraph"])
    
    if uploaded_file is not None:
        os.makedirs("pdfs", exist_ok=True)
        pdf_path = os.path.join("pdfs", uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"📄 Uploaded: {uploaded_file.name}")
        
        if st.button("Summarize PDF"):
            with st.spinner("Reading and summarizing PDF..."):
                try:
                    if pdf_mode == "Full Document":
                        # Use pdfplumber-based method
                        text = get_text_from_pdf(pdf_path)
                        summary = summarize_text(text, summarizer)
                        st.markdown("### 📝 Summary:")
                        for bullet in summary:
                            st.markdown(bullet)
                    else:
                        # Use fitz + headline/paragraph logic
                        raw_text = extract_text_blocks_from_pdf(pdf_path)
                        pairs = extract_headlines_and_paragraphs(raw_text)
                        
                        if not pairs:
                            st.warning("⚠️ Could not extract headline-wise structure. Showing full summary instead.")
                            text = get_text_from_pdf(pdf_path)
                            summary = summarize_text(text, summarizer)
                            st.markdown("### 📝 Summary:")
                            st.write(summary)
                        else:
                            for idx, (headline, paragraph) in enumerate(pairs, 1):
                                summary = summarize_text(paragraph, summarizer)
                                st.markdown(f"#### 🗞️ {headline}")
                                st.write(summary)
                                st.markdown("---")
                except Exception as e:
                    st.error(f"❌ Failed to summarize PDF: {e}")
