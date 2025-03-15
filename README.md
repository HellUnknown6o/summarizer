# Gradio Summarizer

This project is a text summarization tool that uses Gradio for the user interface and Google Generative AI for generating summaries. It can summarize text from both plain text input and PDF files.

## Features

- Summarize plain text input.
- Summarize text extracted from PDF files.
- Adjustable number of summary lines.
- User-friendly interface with Gradio.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/gradio-summarizer.git
    cd gradio-summarizer
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set your Google Generative AI API key:
    ```python
    # Replace 'your_api_key' with your actual API key in app.py
    genai.configure(api_key="your_api_key")
    ```

## Usage

1. Run the application:
    ```sh
    python app.py
    ```

2. Open the Gradio interface in your web browser.

3. Upload a PDF file or paste your text into the provided textbox.

4. Adjust the number of summary lines using the slider.

5. Click the "Submit" button to generate the summary.

## Code Overview

### Extract Text from PDF

```python
// filepath: /home/jainil/workspace/python-projects/gradio summarizer/app.py
import fitz  # PyMuPDF for PDF text extraction
import gradio as gr
import google.generativeai as genai

# ...existing code...

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file using PyMuPDF (fitz)."""
    doc = fitz.open(pdf_file.name)
    text = "\n".join(page.get_text() for page in doc)
    return text
