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



step by step details to ACCESS  the proejct in your local system

 step-1: git clone https://github.com/Bokka-kartik/Blooms-VLITS.git
         cd Blooms-VLITS

 step-2: python -m venv venv
         venv\Scripts\activate  (create and activate a virtual environment)

 step-3: pip install -r requirements.txt  (install dependencies )
 
 step-4: python main.py  (for the working/run the main python file )

 step5: download the large file (You can download them from the shared Google Drive link above and place them in           the correct folders manually.)
 
 step-6: Your project should now be set up and ready to use

keynote: Make sure to activate your environment every time before running the project.

        





