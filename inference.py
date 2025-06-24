import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Load Model
model = BertForSequenceClassification.from_pretrained("fine_tuned_bert_bloom_taxonomy")
tokenizer = BertTokenizer.from_pretrained("fine_tuned_bert_bloom_taxonomy")
device = torch.device("cpu")
model.to(device)
model.eval()

def classify_question(question):
    inputs = tokenizer(question, return_tensors="pt", truncation=True, padding=True, max_length=128)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        predicted_label = torch.argmax(outputs.logits, dim=1).item()
    categories = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
    return categories[predicted_label]

# Example Test
question = "What is the capital of France?"
print(f"Predicted Bloom's Taxonomy Level: {classify_question(question)}")
