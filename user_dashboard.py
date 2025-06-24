# import streamlit as st
# import torch
# from transformers import BertTokenizer, BertForSequenceClassification
# from generate_paper import generate_question_paper
# import os
# import tempfile
# import pythoncom
# import win32com.client
# from streamlit_pdf_viewer import pdf_viewer

# def convert_docx_to_pdf(docx_path):
#     pythoncom.CoInitialize()
#     try:
#         word = win32com.client.Dispatch("Word.Application")
#         word.Visible = False
#         doc = word.Documents.Open(os.path.abspath(docx_path))
#         temp_dir = tempfile.gettempdir()
#         pdf_path = os.path.join(temp_dir, os.path.basename(docx_path).replace(".docx", ".pdf"))
#         doc.SaveAs(pdf_path, FileFormat=17)
#         doc.Close()
#         word.Quit()
#         return pdf_path
#     finally:
#         pythoncom.CoUninitialize()

# @st.cache_resource
# def load_model():
#     model = BertForSequenceClassification.from_pretrained("fine_tuned_bert_bloom_taxonomy")
#     tokenizer = BertTokenizer.from_pretrained("fine_tuned_bert_bloom_taxonomy")
#     device = torch.device("cpu")
#     model.to(device)
#     model.eval()
#     return model, tokenizer, device

# def classify_question(question):
#     model,tokenizer,device = load_model()
#     inputs = tokenizer(question, return_tensors="pt", truncation=True, padding=True, max_length=128)
#     inputs = {key: value.to(device) for key, value in inputs.items()}
#     with torch.no_grad():
#         outputs = model(**inputs)
#         predicted_label = torch.argmax(outputs.logits, dim=1).item()
#     categories = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
#     return categories[predicted_label]

# def validate_bloom_distribution(bloom_dist):
#     total = sum(bloom_dist.values())
#     if not (99.5 <= total <= 100.5):  # Allow for small floating point errors
#         st.error(f"Bloom's taxonomy distribution must sum to 100%. Current sum: {total}%")
#         return False
#     return True

# def validate_difficulty_distribution(difficulty_dist, num_questions):
#     total = sum(difficulty_dist.values())
#     if total != num_questions:
#         st.error(f"Sum of questions across difficulty levels must equal total questions ({num_questions}). Current sum: {total}")
#         return False
#     return True

# def validate_marks_distribution(difficulty_dist, marks_per_diff, total_marks):
#     calculated_total = sum(difficulty_dist[level] * marks_per_diff[level] for level in difficulty_dist.keys())
#     if calculated_total != total_marks:
#         st.error(f"Total marks calculation mismatch. Expected {total_marks}, got {calculated_total}")
#         return False
#     return True

# def show_user_dashboard():
#     st.sidebar.title("***User Dashboard***")
#     if "user_page" not in st.session_state:
#         st.session_state["user_page"] = "classify question"

#     if st.sidebar.button("***Classify Question***"):
#         st.session_state["user_page"] = "classify question"
#     if st.sidebar.button("***Generate Question Paper***"):
#         st.session_state["user_page"] = "generate question paper"
#     if st.sidebar.button("***View Generated Papers***"):
#         st.session_state["user_page"] = "view generated papers"
#     if st.sidebar.button("***Sign Out***"):
#         logout()

#     st.title("***Question Paper Generator***")

#     if st.session_state["user_page"] == "classify question":
#         st.subheader("***Classify a Question***")
#         subject = st.text_input("Enter Subject Name:")
#         user_question = st.text_area("Enter a question:")
#         if st.button("Classify & Save"):
#             if user_question.strip():
#                st.session_state["classified_category"] = classify_question(user_question)
#                st.session_state["confirm_add"] = True 
#         if "confirm_add" not in st.session_state:
#             st.session_state["confirm_add"] = False  # Ensure it is initialized


#     # Your existing logic here
       
#         if st.session_state["confirm_add"]:
#            st.write(f"✅ Question classified as: **{st.session_state['classified_category']}**")
#            confirm = st.button("OK to Save")
#            cancel = st.button("Cancel")   
#            if confirm:
#             # Code to add the classified question to the dataset
#                st.success("✅ Question successfully added to the dataset!")
#                st.session_state["confirm_add"] = False  # Reset the state
#            elif cancel:
#             st.warning("❌ Action canceled.")
#             st.session_state["confirm_add"] = False      
#         else:
#                 st.warning("⚠️ Please enter a valid question!")

#     elif st.session_state["user_page"] == "generate question paper":
#         st.subheader("***📄 Generate a Question Paper***")

#         col1, col2 = st.columns(2)
#         with col1:
#             topic = st.text_input("Enter Subject/Topic:")
#             num_questions = st.number_input("Number of Questions", min_value=1, max_value=50, value=10)
#         with col2:
#             total_marks = st.number_input("Total Marks for Exam", min_value=10, max_value=200, value=100)

#         st.subheader("***Set Bloom's Taxonomy Distribution (%)***")
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             remember = st.number_input("Remember", min_value=0, max_value=100, value=20)
#             understand = st.number_input("Understand", min_value=0, max_value=100, value=20)
#         with col2:
#             apply = st.number_input("Apply", min_value=0, max_value=100, value=20)
#             analyze = st.number_input("Analyze", min_value=0, max_value=100, value=15)
#         with col3:
#             evaluate = st.number_input("Evaluate", min_value=0, max_value=100, value=15)
#             create = st.number_input("Create", min_value=0, max_value=100, value=10)

#         bloom_distribution = {
#             "Remember": remember,
#             "Understand": understand,
#             "Apply": apply,
#             "Analyze": analyze,
#             "Evaluate": evaluate,
#             "Create": create
#         }

#         st.subheader("***Set Difficulty Level Distribution (Number of Questions)***")
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             easy = st.number_input("Easy", min_value=0, max_value=num_questions, value=5)
#         with col2:
#             medium = st.number_input("Medium", min_value=0, max_value=num_questions, value=3)
#         with col3:
#             hard = st.number_input("Hard", min_value=0, max_value=num_questions, value=2)

#         difficulty_distribution = {
#             "Easy": easy,
#             "Medium": medium,
#             "Hard": hard
#         }

#         st.subheader("***Set Marks per Question Difficulty Level***")
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             easy_marks = st.number_input("Marks for Easy", min_value=1, max_value=10, value=2)
#         with col2:
#             medium_marks = st.number_input("Marks for Medium", min_value=1, max_value=15, value=5)
#         with col3:
#             hard_marks = st.number_input("Marks for Hard", min_value=1, max_value=20, value=10)

#         marks_per_difficulty = {
#             "Easy": easy_marks,
#             "Medium": medium_marks,
#             "Hard": hard_marks
#         }

#         if st.button("***Generate***"):
#             if not topic.strip():
#                 st.warning("Please enter a valid topic!")
#                 return

#             # Validate all distributions
#             if not validate_bloom_distribution(bloom_distribution):
#                 return
#             if not validate_difficulty_distribution(difficulty_distribution, num_questions):
#                 return
#             if not validate_marks_distribution(difficulty_distribution, marks_per_difficulty, total_marks):
#                 return

#             try:
#                 os.makedirs("generated_papers", exist_ok=True)
#                 file_name = generate_question_paper(
#                     topic, num_questions, total_marks,
#                     bloom_distribution, difficulty_distribution, marks_per_difficulty
#                 )
                
#                 with open(file_name, "rb") as file:
#                     st.download_button(
#                         label="📥 Download Question Paper",
#                         data=file,
#                         file_name=os.path.basename(file_name)
#                     )
                
#                 st.success(f"✅ Question paper generated successfully!")
#             except Exception as e:
#                 st.error(f"Error generating question paper: {str(e)}")

#     # elif st.session_state["user_page"] == "view generated papers":
#     #     st.subheader("***📂 View Generated Question Papers***")
#     #     if not os.path.exists("generated_papers"):
#     #         st.warning("No generated papers found.")
#     #     else:
#     #         files = os.listdir("generated_papers")
#     #         if not files:
#     #             st.warning("No generated papers found.")
#     #         else:
#     #             for file in files:
#     #                 with st.container(border=True):
#     #                     file_path = os.path.join("generated_papers", file)
#     #                     st.write(f"📄 **{file}**")
#     #                     col1, col2 = st.columns(2)
#     #                     with col1:
#     #                         with open(file_path, "rb") as f:
#     #                             st.download_button(
#     #                                 label="***Download***",
#     #                                 data=f,
#     #                                 file_name=file,
#     #                                 key=f"download_{file}"
#     #                             )
#     #                     with col2:
#     #                         file_to_show = file.split("_")
#     #                         if st.button(f"***Preview {file_to_show[0]}***"):
#     #                             pdf_file_path = convert_docx_to_pdf(file_path)
#     #                             preview(pdf_file_path)
#     elif st.session_state["user_page"] == "view generated papers":
#         st.subheader("***📂 View Generated Question Papers***")
#         if not os.path.exists("generated_papers"):
#             st.warning("No generated papers found.")
#         else:
#             files = os.listdir("generated_papers")
#             if not files:
#                 st.warning("No generated papers found.")
#             else:
#                 for file in files:
#                     with st.container(border=True):
#                         file_path = os.path.join("generated_papers", file)
#                         st.write(f"📄 **{file}**")
#                         col1, col2 = st.columns(2)
#                         with col1:
#                             with open(file_path, "rb") as f:
#                                 st.download_button(
#                                     label="***Download***",
#                                     data=f,
#                                     file_name=file,
#                                     key=f"download_{file}"
#                                 )
#                         with col2:
#                             # Split filename to get subject and date
#                             file_parts = file.replace('.docx', '').split('_')
#                             subject = file_parts[0]
#                             date = file_parts[1] if len(file_parts) > 1 else "Unknown Date"
                            
#                             if st.button(f"***Preview {subject} ({date})***"):
#                                 pdf_file_path = convert_docx_to_pdf(file_path)
#                                 preview(pdf_file_path)
# @st.dialog("Preview", width="large")
# def preview(pdf_file_path):
#     pdf_viewer(pdf_file_path)

# def logout():
#     st.session_state["logged_in"] = False

import streamlit as st
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from generate_paper import generate_question_paper
import os
import tempfile
import pythoncom
import win32com.client
import sqlite3
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
from auth import DB_PATH  
DATASET_FOLDER = "dataset/"

def store_paper_record(username, subject, file_path):
    """Stores generated paper details in the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS generated_papers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        subject TEXT,
                        file_path TEXT,
                        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    cursor.execute("INSERT INTO generated_papers (username, subject, file_path) VALUES (?, ?, ?)",
                   (username, subject, file_path))

    conn.commit()
    conn.close()
def convert_docx_to_pdf(docx_path):
    pythoncom.CoInitialize()
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(os.path.abspath(docx_path))
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, os.path.basename(docx_path).replace(".docx", ".pdf"))
        doc.SaveAs(pdf_path, FileFormat=17)
        doc.Close()
        word.Quit()
        return pdf_path
    finally:
        pythoncom.CoUninitialize()

@st.cache_resource
def load_model():
    model = BertForSequenceClassification.from_pretrained("fine_tuned_bert_bloom_taxonomy")
    tokenizer = BertTokenizer.from_pretrained("fine_tuned_bert_bloom_taxonomy")
    device = torch.device("cpu")
    model.to(device)
    model.eval()
    return model, tokenizer, device

def classify_question(question):
    model,tokenizer,device = load_model()
    inputs = tokenizer(question, return_tensors="pt", truncation=True, padding=True, max_length=128)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        predicted_label = torch.argmax(outputs.logits, dim=1).item()
    categories = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
    return categories[predicted_label]

def validate_bloom_distribution(bloom_dist):
    total = sum(bloom_dist.values())
    if not (99.5 <= total <= 100.5):  
        st.error(f"Bloom's taxonomy distribution must sum to 100%. Current sum: {total}%")
        return False
    return True

def validate_difficulty_distribution(difficulty_dist, num_questions):
    total = sum(difficulty_dist.values())
    if total != num_questions:
        st.error(f"Sum of questions across difficulty levels must equal total questions ({num_questions}). Current sum: {total}")
        return False
    return True

def validate_marks_distribution(difficulty_dist, marks_per_diff, total_marks):
    calculated_total = sum(difficulty_dist[level] * marks_per_diff[level] for level in difficulty_dist.keys())
    if calculated_total != total_marks:
        st.error(f"Total marks calculation mismatch. Expected {total_marks}, got {calculated_total}")
        return False
    return True

def show_user_dashboard():
      
    st.sidebar.title("***User Dashboard***")
    if "user_page" not in st.session_state:
        st.session_state["user_page"] = "classify question"

    if st.sidebar.button("***Classify Question***"):
        st.session_state["user_page"] = "classify question"
    if st.sidebar.button("***Generate Question Paper***"):
        st.session_state["user_page"] = "generate question paper"
    if st.sidebar.button("***View Generated Papers***"):
        st.session_state["user_page"] = "view generated papers"
    if st.sidebar.button("***Sign Out***"):
        logout()

    st.title("***Question Paper Generator***")

    if st.session_state["user_page"] == "classify question":
        DIFFICULTY_LEVELS=["Easy","Medium","Hard"]
        st.subheader("***Classify a Question***")
        subject = st.text_input("Enter Subject Name:")
        difficulty = st.selectbox("Select Difficulty Level", DIFFICULTY_LEVELS)

        user_question = st.text_area("Enter a question:")
        if st.button("Classify & Save"):
            if user_question.strip():
                category = classify_question(user_question)
                st.success(f"✅ Question classified as: **{category}** and saved to the dataset!")
                datasets = [f for f in os.listdir(DATASET_FOLDER) if f.endswith(".csv")]
                if subject+".csv" not in datasets:
                    st.warning(f"Please ask Admin to upload a Questions paper for subject {subject} first to add your question into dataset.")
                else:
                    add_to_dataset(subject,user_question,difficulty,category)

            else:
                st.warning("⚠️ Please enter a valid question!")

    elif st.session_state["user_page"] == "generate question paper":
        st.subheader("***📄 Generate a Question Paper***")

        col1, col2 = st.columns(2)
        with col1:
            topic = st.text_input("Enter Subject/Topic:")
            num_questions = st.number_input("Number of Questions", min_value=1, max_value=50, value=10)
        with col2:
            total_marks = st.number_input("Total Marks for Exam", min_value=10, max_value=200, value=100)

        st.subheader("***Set Bloom's Taxonomy Distribution (%)***")
        col1, col2, col3 = st.columns(3)
        with col1:
            remember = st.number_input("Remember", min_value=0, max_value=100, value=20)
            understand = st.number_input("Understand", min_value=0, max_value=100, value=20)
        with col2:
            apply = st.number_input("Apply", min_value=0, max_value=100, value=20)
            analyze = st.number_input("Analyze", min_value=0, max_value=100, value=15)
        with col3:
            evaluate = st.number_input("Evaluate", min_value=0, max_value=100, value=15)
            create = st.number_input("Create", min_value=0, max_value=100, value=10)

        bloom_distribution = {
            "Remember": remember,
            "Understand": understand,
            "Apply": apply,
            "Analyze": analyze,
            "Evaluate": evaluate,
            "Create": create
        }

        st.subheader("***Set Difficulty Level Distribution (Number of Questions)***")
        col1, col2, col3 = st.columns(3)
        with col1:
            easy = st.number_input("Easy", min_value=0, max_value=num_questions, value=5)
        with col2:
            medium = st.number_input("Medium", min_value=0, max_value=num_questions, value=3)
        with col3:
            hard = st.number_input("Hard", min_value=0, max_value=num_questions, value=2)

        difficulty_distribution = {
            "Easy": easy,
            "Medium": medium,
            "Hard": hard
        }

        st.subheader("***Set Marks per Question Difficulty Level***")
        col1, col2, col3 = st.columns(3)
        with col1:
            easy_marks = st.number_input("Marks for Easy", min_value=1, max_value=10, value=2)
        with col2:
            medium_marks = st.number_input("Marks for Medium", min_value=1, max_value=15, value=5)
        with col3:
            hard_marks = st.number_input("Marks for Hard", min_value=1, max_value=20, value=10)

        marks_per_difficulty = {
            "Easy": easy_marks,
            "Medium": medium_marks,
            "Hard": hard_marks
        }

        if st.button("***Generate***"):
            if not topic.strip():
                st.warning("Please enter a valid topic!")
                return

            if not validate_bloom_distribution(bloom_distribution):
                return
            if not validate_difficulty_distribution(difficulty_distribution, num_questions):
                return
            if not validate_marks_distribution(difficulty_distribution, marks_per_difficulty, total_marks):
                return

            try:
                os.makedirs("generated_papers", exist_ok=True)
                file_name = generate_question_paper(
                    topic, num_questions, total_marks,
                    bloom_distribution, difficulty_distribution, marks_per_difficulty
                )
                store_paper_record(st.session_state["username"], topic, file_name)
                
                with open(file_name, "rb") as file:
                    st.download_button(
                        label="📥 Download Question Paper",
                        data=file,
                        file_name=os.path.basename(file_name)
                    )
                
                st.success(f"✅ Question paper generated successfully!")
            except Exception as e:
                st.error(f"Error generating question paper: {str(e)}")
    elif st.session_state["user_page"] == "view generated papers":
        st.subheader("***📂 View Your Generated Question Papers***")
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, subject, file_path, generated_at 
            FROM generated_papers 
            WHERE username = ? 
            ORDER BY generated_at DESC
        """, (st.session_state["username"],))
        papers = cursor.fetchall()
        conn.close()
        
        if not papers:
            st.warning("You haven't generated any papers yet.")
        else:
            for paper in papers:
                paper_id, subject, file_path, generated_at = paper
                
                if os.path.exists(file_path):
                    with st.container(border=True):
                        file_name = os.path.basename(file_path)
                        st.write(f"📄 **{file_name}** - Generated on {generated_at}")
                        col1, col2 = st.columns(2)
                        with col1:
                            with open(file_path, "rb") as f:
                                st.download_button(
                                    label="***Download***",
                                    data=f,
                                    file_name=file_name,
                                    key=f"download_{paper_id}"
                                )
                        with col2:
                            if st.button(f"***Preview {subject}***", key=f"preview_{paper_id}"):
                                pdf_file_path = convert_docx_to_pdf(file_path)
                                preview(pdf_file_path)
@st.dialog("Preview", width="large")
def preview(pdf_file_path):
    pdf_viewer(pdf_file_path)
@st.dialog("Add Question to dataset",width="small")
def add_to_dataset(subject,user_question,difficulty,category):
    st.header("***Subject***")
    st.write(subject)
    st.header("***Question***")
    st.write(user_question)
    st.header("***Difficulty Level***")
    st.write(difficulty)
    st.header("***Blooms Level***")
    st.write(category)
    new_data = pd.DataFrame([{
                        "question": user_question,
                        "bloom_taxonomy_level": category,
                        "difficulty": difficulty
                    }])
    if st.button("***Add Question***"):
        try:
            dataset_path = os.path.join(DATASET_FOLDER, f"{subject}.csv")
            
            if os.path.exists(dataset_path):
                df_existing = pd.read_csv(dataset_path)
                df_combined = pd.concat([df_existing, new_data], ignore_index=True)
            else:
                df_combined = new_data

            df_combined.to_csv(dataset_path, index=False)
            st.success(f"Question added to {subject}.csv!")
        except Exception as e:
            st.error(f"Error adding question: {str(e)}")


def logout():
    st.session_state["logged_in"] = False