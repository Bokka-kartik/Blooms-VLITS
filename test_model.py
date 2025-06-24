import torch
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification

# Load Model
model = BertForSequenceClassification.from_pretrained("fine_tuned_bert_bloom_taxonomy")
tokenizer = BertTokenizer.from_pretrained("fine_tuned_bert_bloom_taxonomy")
device = torch.device("cpu")

model.to(device)
model.eval()

# Load Dataset
df = pd.read_csv("bloom_taxonomy_dataset.csv")

# Function to classify a question
def classify_question(question):
    inputs = tokenizer(question, return_tensors="pt", truncation=True, padding=True, max_length=128)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        predicted_label = torch.argmax(outputs.logits, dim=1).item()
    categories = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
    return categories[predicted_label]

# Test Model on 10 Questions
df_sample = df.sample(227)  # Randomly select 10 questions
results = []
for question in df_sample["question"]:
    predicted_category = classify_question(question)
    results.append({"Question": question, "Predicted Level": predicted_category})

# Convert results to DataFrame
results_df = pd.DataFrame(results)
print(results_df)

# Save results
results_df.to_csv("test_results.csv", index=False)
print("Test results saved to test_results.csv")


