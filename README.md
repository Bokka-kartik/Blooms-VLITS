# Blooms VLITS

A web application that uses a fine-tuned BERT model to classify questions according to Bloom’s Taxonomy. Useful for educational institutions to analyze and generate question papers intelligently.

 Features
- Upload questions for Bloom level classification
- Admin and student dashboards
- Question generation using Bloom taxonomy levels
- Authentication for students/admins

## Project Structure

main.py # Entry point
classifier.py # Bloom level classification logic
generate_paper.py # Auto-generate question papers
train_model.py # (Optional) training logic
inference.py # Model inference
admin_dashboard.py # Admin panel
user_dashboard.py # Student interface
auth.py # Authentication logic
bloom_taxonomy_dataset.csv # Sample dataset


 `model.safetensors` file not included — please download separately from [Google Drive](https://drive.google.com/drive/folders/1-gOBLCihfu37dRkehKQCXRUwhLKZRuyH?usp=sharing).


## ⚙ Installation
pip install -r requirements.txt
python main.py




