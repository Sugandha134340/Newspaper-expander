# Newspaper Article Summarizer

**Problem Statement**

In today’s fast-paced world, people often do not have the time to sit and read entire newspapers, even though staying informed is crucial. This is especially true for busy individuals who want to stay updated without spending too much time, and for students preparing for public service examinations like UPSC, TNPSC, etc., who need to regularly follow current affairs. Such aspirants typically read newspapers daily and make notes for quick revisions later. However, going through full-length articles and manually noting down key points is time-consuming.

To address this problem, we created a tool that helps users extract and summarize essential news content automatically from various sources. This allows both busy professionals and competitive exam aspirants to stay informed quickly, revise effectively, and even prepare digital notes with ease.

**Approach & Solution**

The application takes long-form newspaper articles and intelligently extracts the most relevant information in a concise format. It uses Natural Language Processing (NLP) to summarize paragraphs and removes unnecessary details. The approach is tailored to support three different input types:

1. **Direct URL of a news article** – Users can paste the link to a specific article, and the app extracts and summarizes it.
2. **URL of a news homepage** – The app fetches all headlines on that homepage, extracts their individual article links, and summarizes each article.
3. **PDF upload of a newspaper** – Users can upload a PDF version of a newspaper. The app processes the PDF, extracts article headlines and paragraphs using heuristics, and summarizes them.

In each case, the summarized content is broken down into point-wise format for easier reading, reviewing, and note-making.

**Features**

- Supports multiple input types: individual article URLs, full news website homepage URLs, and uploaded newspaper PDFs.
- Extracts headlines and articles from raw text using regex and heuristics.
- Summarizes long paragraphs using a pre-trained transformer model (BART).
- Breaks summary into meaningful bullet points for clarity and readability.
- Clean user interface built with Streamlit.
- Automatically skips irrelevant or repetitive lines during summarization.
- Ideal for civil service aspirants and time-constrained readers.

**Tech Stack**

- **Python** – Backend logic and processing
- **PyMuPDF (fitz)** – PDF text extraction
- **Newspaper3k** – News content extraction from URLs
- **BeautifulSoup** – Scraping headlines and links from homepage URLs
- **Hugging Face Transformers** – Text summarization using BART model
- **Streamlit** – Web app framework for creating the user interface

**Installation Note**

Due to file size limitations on GitHub, the Spacy language model file (en_core_web_sm-3.8.0-py3-none-any.whl) is not included in the repository.
Please follow the steps below to install it manually:

Download the wheel file en_core_web_sm-3.8.0-py3-none-any.whl from the shared source or place it in the project root directory.

Then run the following command to install it:

bash
pip install en_core_web_sm-3.8.0-py3-none-any.whl

Finally, link the model using:

bash
python -m spacy link en_core_web_sm en_core_web_sm

**Run Instructions**

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sugandha134340/Newspaper-expander.git
   cd newspaper-expander
2. **Set up a virtual environment (recommended)**
    ```bash
    python -m venv venv

3. **Activate the virtual environment**

    ```bash
    On Windows:
        .\venv\Scripts\activate

4. **Install dependencies**
    ```
    bashpip install -r requirements.txt

5. **Run the application**

    ```bash
    streamlit run app.py