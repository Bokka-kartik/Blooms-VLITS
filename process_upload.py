import fitz  # PyMuPDF for PDF extraction
import docx
import pandas as pd
import os
import sqlite3
# from classifier import classify_question
import streamlit as st
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import docx
import re

# Load the fine-tuned model and tokenizer
@st.cache_resource
def load_model():
    model = BertForSequenceClassification.from_pretrained("fine_tuned_bert_bloom_taxonomy")
    tokenizer = BertTokenizer.from_pretrained("fine_tuned_bert_bloom_taxonomy")
    device = torch.device("cpu")
    model.to(device)
    model.eval()
    return model, tokenizer, device

model, tokenizer, device = load_model()

# Function to classify a question
def classify_question(question):
    inputs = tokenizer(question, return_tensors="pt", truncation=True, padding=True, max_length=128)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        predicted_label = torch.argmax(outputs.logits, dim=1).item()

    categories = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
    return categories[predicted_label]

DB_PATH = "new_database.db"
DATASET_FOLDER = "dataset/"
UPLOADS_FOLDER = "uploads/"

os.makedirs(DATASET_FOLDER, exist_ok=True)
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return [line.strip() for line in text.split("\n") if line.strip()]

def extract_text_from_docx(docx_path):
    """Extracts questions and difficulty levels from a DOCX file where difficulty is at the end."""
    doc = docx.Document(docx_path)
    extracted_data = []

    for para in doc.paragraphs:
        text = para.text.strip()

        # Skip empty lines
        if not text:
            continue

        # Extract difficulty level using the updated function
        difficulty = extract_difficulty(text)
        question = re.sub(r"(?:\(|\[)?(Easy|Medium|Hard)(?:\)|\])?$", "", text).strip()  # Remove difficulty from question

        extracted_data.append({"question": question[2:], "difficulty": difficulty})

    return extracted_data  # Returns a list of dictionaries with question and difficultyimport re  # Add regex for extracting difficulty level
#extracting difficulty level from question text
def extract_difficulty(question):
    """Extracts difficulty level from the question text, supporting different cases and formats."""
    match = re.search(r"(?:\(|\[)?(Easy|Medium|Hard)(?:\)|\])?$", question, re.IGNORECASE)
    return match.group(1).capitalize() if match else "Unknown"
#saving the extracted questions to a dataset
def save_to_dataset(subject, questions):
    """Saves extracted questions with difficulty level into the dataset."""
    dataset_path = os.path.join(DATASET_FOLDER, f"{subject}.csv")

    classified_data = []
    for item in questions:
        q_text = item["question"]
        difficulty = item["difficulty"]
        bloom_level = classify_question(q_text)  # Use existing function to classify Bloom's taxonomy
        
        classified_data.append({"question": q_text, "difficulty": difficulty, "bloom_taxonomy_level": bloom_level})

    df_new = pd.DataFrame(classified_data)

    if os.path.exists(dataset_path):
        df_existing = pd.read_csv(dataset_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_csv(dataset_path, index=False)
    return dataset_path
def create_upload_table():
    """Ensures the uploads table exists before storing data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS uploads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        admin TEXT,
                        subject TEXT,
                        file_name TEXT,
                        dataset_path TEXT,
                        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def store_upload_record(admin_name, subject, file_name, dataset_path):
    """Stores file upload details in the SQLite database."""
    create_upload_table()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO uploads (admin, subject, file_name, dataset_path) VALUES (?, ?, ?, ?)",
                   (admin_name, subject, file_name, dataset_path))

    conn.commit()
    conn.close()
