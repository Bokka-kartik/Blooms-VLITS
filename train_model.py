# import torch
# from torch.utils.data import DataLoader, Dataset
# # from transformers import BertTokenizer, BertForSequenceClassification, AdamWfrom 
# from transformers import BertTokenizer, BertForSequenceClassification
# from torch.optim import AdamW  # Use PyTorch's AdamW

# # Define the model (Make sure this comes before defining the optimizer)
# model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=5)

# # Define the optimizer
# optimizer = AdamW(model.parameters(), lr=2e-5)

# from sklearn.model_selection import train_test_split
# import pandas as pd
# import logging

# # Load Dataset
# df = pd.read_csv("bloom_taxonomy_dataset.csv")

# # Split Dataset
# train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

# # Load BERT Tokenizer
# tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# # Dataset Class
# class BloomTaxonomyDataset(Dataset):
#     def __init__(self, dataframe, tokenizer, max_len=128):
#         self.data = dataframe
#         self.tokenizer = tokenizer
#         self.max_len = max_len

#     def __len__(self):
#         return len(self.data)

#     def __getitem__(self, index):
#         question = self.data.iloc[index]['question']
#         label = self.data.iloc[index]['bloom_taxonomy_level']
#         encoding = self.tokenizer.encode_plus(
#             question, add_special_tokens=True, max_length=self.max_len,
#             return_token_type_ids=False, padding='max_length', truncation=True,
#             return_attention_mask=True, return_tensors='pt',
#         )
#         return {
#             'input_ids': encoding['input_ids'].flatten(),
#             'attention_mask': encoding['attention_mask'].flatten(),
#             'labels': torch.tensor(self._label_to_index(label), dtype=torch.long)
#         }


#     def _label_to_index(self, label):
#         label_map = {"Remember": 0, "Understand": 1, "Apply": 2, "Analyze": 3, "Evaluate": 4, "Create": 5}
#         label = label.strip()  # Remove extra spaces
#         return label_map[label]

# # Create DataLoaders
# def create_data_loader(df, tokenizer, batch_size=16):
#     ds = BloomTaxonomyDataset(df, tokenizer)
#     return DataLoader(ds, batch_size=batch_size)

# train_data_loader = create_data_loader(train_df, tokenizer)
# val_data_loader = create_data_loader(val_df, tokenizer)

# # Load BERT Model
# model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=6)
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# # Training Setup
# optimizer = AdamW(model.parameters(), lr=1e-5)  # Lower learning rate for better training
# loss_fn = torch.nn.CrossEntropyLoss().to(device)

# # Training Function
# def train_epoch(model, data_loader, loss_fn, optimizer, device):
#     model.train()
#     total_loss = 0

#     for batch in data_loader:
#         input_ids = batch['input_ids'].to(device)
#         attention_mask = batch['attention_mask'].to(device)
#         labels = batch['labels'].to(device)

#         optimizer.zero_grad()
#         outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
#         loss = outputs.loss
#         total_loss += loss.item()
#         loss.backward()
#         optimizer.step()

#     return total_loss / len(data_loader)

# # Training Loop
# EPOCHS = 5
# for epoch in range(EPOCHS):
#     train_loss = train_epoch(model, train_data_loader, loss_fn, optimizer, device)
#     print(f'Epoch {epoch+1}: Train Loss = {train_loss:.4f}')

# # Save Model
# model.save_pretrained("fine_tuned_bert_bloom_taxonomy")
# tokenizer.save_pretrained("fine_tuned_bert_bloom_taxonomy")
# print("Fine-tuned model saved.")

import torch
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertForSequenceClassification
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
import pandas as pd
import transformers

# Suppress unnecessary warnings
transformers.logging.set_verbosity_error()

# Load Dataset
df = pd.read_csv("bloom_taxonomy_dataset.csv")

# Standardize the capitalization of the 'bloom_taxonomy_level' column
df['bloom_taxonomy_level'] = df['bloom_taxonomy_level'].str.title()

# Split Dataset
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

# Load BERT Tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Label Mapping
LABEL_MAP = {
    "Remember": 0, "Understand": 1, "Apply": 2, 
    "Analyze": 3, "Evaluate": 4, "Create": 5
}

# Dataset Class
class BloomTaxonomyDataset(Dataset):
    def __init__(self, dataframe, tokenizer, max_len=128):
        self.data = dataframe
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        question = self.data.iloc[index]['question']
        label = self.data.iloc[index]['bloom_taxonomy_level'].strip()

        # Convert label to index
        label_idx = LABEL_MAP.get(label, -1)

        if label_idx == -1:
            raise ValueError(f"Unknown label '{label}' found in dataset!")

        encoding = self.tokenizer.encode_plus(
            question,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': torch.tensor(label_idx, dtype=torch.long)
        }

# Create DataLoaders
def create_data_loader(df, tokenizer, batch_size=16):
    ds = BloomTaxonomyDataset(df, tokenizer)
    return DataLoader(ds, batch_size=batch_size, shuffle=True)

train_data_loader = create_data_loader(train_df, tokenizer)
val_data_loader = create_data_loader(val_df, tokenizer)

# Load BERT Model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(LABEL_MAP))
model.to(device)

# Training Setup
optimizer = AdamW(model.parameters(), lr=1e-5)
loss_fn = torch.nn.CrossEntropyLoss().to(device)

# Training Function
def train_epoch(model, data_loader, loss_fn, optimizer, device):
    model.train()
    total_loss = 0

    for batch in data_loader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        optimizer.zero_grad()
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        total_loss += loss.item()
        loss.backward()
        optimizer.step()

    return total_loss / len(data_loader)

# Training Loop
EPOCHS = 5
for epoch in range(EPOCHS):
    train_loss = train_epoch(model, train_data_loader, loss_fn, optimizer, device)
    print(f'Epoch {epoch+1}: Train Loss = {train_loss:.4f}')

# Save Model
model.save_pretrained("fine_tuned_bert_bloom_taxonomy")
tokenizer.save_pretrained("fine_tuned_bert_bloom_taxonomy")
print("Fine-tuned model saved successfully.")
