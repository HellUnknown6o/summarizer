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
    

### Chunk Text

```python
# filepath: /home/jainil/workspace/python-projects/gradio summarizer/app.py
# ...existing code...

def chunk_text(text, chunk_size=3000):
    """Splits text into smaller chunks to fit within model limits."""
    words = text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks
```

### Summarize Text

```python
# filepath: /home/jainil/workspace/python-projects/gradio summarizer/app.py
# ...existing code...

def summarize_text(input_text, num_lines):
    """Summarizes the given text."""
    response = model.generate_content(
        f"Summarize this text in {num_lines} lines:\n\n{input_text}",
        generation_config={"temperature": 0.5, "max_output_tokens": num_lines * 20}
    )
    return response.text if response.text else "Error in response."
```

### Process PDF

```python
# filepath: /home/jainil/workspace/python-projects/gradio summarizer/app.py
# ...existing code...

def process_pdf(pdf_file, num_lines):
    """Processes PDF, extracts text, chunks it, and summarizes each chunk before merging."""
    full_text = extract_text_from_pdf(pdf_file)
    
    # Chunk the text
    chunks = chunk_text(full_text)
    chunk_summaries = []

    for chunk in chunks:
        summary = summarize_text(chunk, num_lines)  # Summarize each chunk
        chunk_summaries.append(summary)
    
    # Generate final summary from chunk summaries
    final_summary = summarize_text(" ".join(chunk_summaries), num_lines)
    
    return final_summary
```

### Gradio Interface

```python
# filepath: /home/jainil/workspace/python-projects/gradio summarizer/app.py
# ...existing code...

iface = gr.Interface(
    fn=process_pdf,
    inputs=[
        gr.File(label="Upload PDF"),
        gr.Slider(minimum=1, maximum=10, step=1, value=3, label="Number of Summary Lines")
    ],
    outputs=gr.Textbox(lines=10, label="Summarized Text"),
)

# 🎬 Launch the app
iface.launch()
```

