# import gradio as gr
# from transformers import pipeline

# # Initialize the model (Move this OUTSIDE the function)
# model = pipeline("text-generation", model="gpt2")

# def process_text(input_text):
#     response = model.generate(input_text)  # Ensure this function generates a full response
#     full_text = "".join(response)  # Join chunks if needed
#     print("Full response:", full_text)
#     return full_text

# iface = gr.Interface(
#     fn=process_text,
#     inputs=gr.Textbox(),
#     outputs=gr.Textbox(lines=5),  # Increase lines to fit longer text
# )



# basic code for getting summary via created prompt from our summarizer 

# import gradio as gr
# import google.generativeai as genai

# # 🔑 Set API key
# genai.configure(api_key="AIzaSyCy1V0_UQOiz23hTYl41wwGlZLs6W3-XoA")

# # 🔍 Load Model
# model = genai.GenerativeModel("gemini-2.0-flash")

# def clean_summary(text, num_lines):
#     """Trims the summary to the specified number of lines."""
#     lines = text.split("\n")
#     return "\n".join(lines[:num_lines])  # Keep only the desired number of lines

# def process_text(input_text, num_lines):
#     response = model.generate_content(
#         f"Summarize this text in {num_lines} lines:\n\n{input_text}",
#         generation_config={
#             "temperature": 0.5,  
#             "max_output_tokens": num_lines * 20  # Adjust based on line count
#         }
#     )
#     return clean_summary(response.text, num_lines)

# # 🌟 Create Gradio UI
# iface = gr.Interface(
#     fn=process_text,
#     inputs=[
#         gr.Textbox(placeholder="Paste your text here..."),  
#         gr.Slider(minimum=1, maximum=10, step=1, value=3, label="Number of Lines")
#     ],
#     outputs=gr.Textbox(lines=10),
# )

# # 🎬 Launch the app
# iface.launch()

# code for summarizing via pdf too 

import os
import fitz  # PyMuPDF for PDF text extraction
import gradio as gr
import google.generativeai as genai

# api key for gemini

# 🔑 Configure API key
genai.configure(api_key="api_key_gem")
# Load Model
model = genai.GenerativeModel("gemini-2.0-flash")

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file using PyMuPDF (fitz)."""
    doc = fitz.open(pdf_file.name)
    text = "\n".join(page.get_text() for page in doc)
    return text

def chunk_text(text, chunk_size=3000):
    """Splits text into smaller chunks to fit within model limits."""
    words = text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def summarize_text(input_text, num_lines):
    """Summarizes the given text."""
    response = model.generate_content(
        f"Summarize this text in {num_lines} lines:\n\n{input_text}",
        generation_config={"temperature": 0.5, "max_output_tokens": num_lines * 20}
    )
    return response.text if response.text else "Error in response."

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

# 🎯 Gradio UI
iface = gr.Interface(
    fn=process_pdf,
    inputs=[
        gr.File(label="Upload PDF"),
        gr.Slider(minimum=1, maximum=10, step=1, value=3, label="Number of Summary Lines")
    ],
    outputs=gr.Textbox(lines=10, label="Summarized Text"),
)



# 🎬 Launch the app
# Get the port from the environment variable
port = int(os.environ.get('PORT', 8080))

# 🎬 Launch the app
iface.launch(server_name="0.0.0.0", server_port=port)