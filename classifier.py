# import spacy
import torch
# import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
# import os
# import logging


# Load fine-tuned model
model = BertForSequenceClassification.from_pretrained("fine_tuned_bert_bloom_taxonomy")
tokenizer = BertTokenizer.from_pretrained("fine_tuned_bert_bloom_taxonomy")
device = torch.device("cpu")
model.to(device)
model.eval()

def classify_question(question):
    """
    Predicts Bloom’s Taxonomy category for a given question.
    
    Args:
        question (str): The input question to classify.
    
    Returns:
        str: The predicted Bloom's Taxonomy category.
    """
    inputs = tokenizer(question, return_tensors="pt", truncation=True, padding=True, max_length=128)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        predicted_label = torch.argmax(outputs.logits, dim=1).item()

    categories = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
    return categories[predicted_label]



# # Load NLP Model
# nlp = spacy.load("en_core_web_sm")

# # Load BERT Model & Tokenizer
# tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
# model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=6)

# # Force Model to Run on CPU (Fix RuntimeError)
# device = torch.device("cpu")
# model.to(device)
# model.eval()

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# # Define Dataset Path
# DATASET_PATH = "dataset.csv"

# # Bloom's Taxonomy categories
# categories = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]

# def classify_question(question):
#     """
#     Predicts Bloom’s Taxonomy category for a given question.
    
#     Args:
#         question (str): The input question to classify.
    
#     Returns:
#         str: The predicted Bloom's Taxonomy category.
#     """
#     # Log the input question
#     logging.debug(f"Classifying question: {question}")

#     # Tokenize the input question
#     inputs = tokenizer(
#         question,
#         return_tensors="pt",
#         truncation=True,
#         padding=True,
#         max_length=128
#     )
#     inputs = {key: value.to(device) for key, value in inputs.items()}  # Move inputs to CPU

#     # Perform inference
#     with torch.no_grad():
#         outputs = model(**inputs)
#         predicted_label = torch.argmax(outputs.logits, dim=1).item()

#     # Map the predicted label to the corresponding Bloom's Taxonomy category
#     category = categories[predicted_label]

#     # Log the predicted category
#     logging.debug(f"Predicted label: {predicted_label}")
#     logging.debug(f"Predicted category: {category}")

#     return category
def preprocess_question(question):
    """Tokenization and stopword removal."""
    doc = nlp(question.lower())
    return " ".join([token.text for token in doc if not token.is_stop])

# def classify_question(question):
#     """Predicts Bloom’s Taxonomy category and stores the question."""
#     logging.debug(f"Classifying question: {question}")
#     inputs = tokenizer(question, return_tensors="pt", truncation=True, padding=True, max_length=128)
#     inputs = {key: value.to(device) for key, value in inputs.items()}  # Move to CPU
#     outputs = model(**inputs)
#     predicted_label = torch.argmax(outputs.logits, dim=1).item()
#     logging.debug(f"Predicted label: {predicted_label}")

#     # Bloom’s Taxonomy Levels
#     categories = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
#     category = categories[predicted_label]
#     logging.debug(f"Predicted category: {category}")

#     # Save to Dataset
#     save_question(question, category)

#     return category

def save_question(question, category):
    """Saves the classified question to dataset.csv."""
    new_entry = pd.DataFrame([[question, category]], columns=["question", "bloom_taxonomy_level"])

    if os.path.exists(DATASET_PATH):
        existing_data = pd.read_csv(DATASET_PATH)
        updated_data = pd.concat([existing_data, new_entry], ignore_index=True)
        updated_data.to_csv(DATASET_PATH, index=False)
    else:
        new_entry.to_csv(DATASET_PATH, index=False)