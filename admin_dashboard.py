# import streamlit as st
# import os
# import pandas as pd
# import sqlite3
# import uuid
# from process_upload import extract_text_from_pdf, extract_text_from_docx, save_to_dataset, store_upload_record

# DB_PATH = "new_database.db"
# DATASET_FOLDER = "dataset/"
# UPLOADS_FOLDER = "uploads/"

# os.makedirs(DATASET_FOLDER, exist_ok=True)
# os.makedirs(UPLOADS_FOLDER, exist_ok=True)
# @st.dialog("Dataset Preview",width="large")
# def show_dataset(dataset_path):
#     df=pd.read_csv(dataset_path)
#     df = pd.read_csv(dataset_path)
#     # Reset index and start numbering from 1
#     df = df.reset_index(drop=True)
#     df.index = df.index + 1
#     st.write(df.tail(len(df)))
#     # st.dataframe(df.style.highlight_max())
# def show_admin_dashboard():
#     # Custom CSS for Sidebar Buttons
#     st.markdown(
#     """
#     <style>
#         /* Styling for all buttons (Login, Register, etc.) */
#         div.stButton > button, div.stDownloadButton > button {
#             width: 200px !important;  /* Fixed width */
#             height: 45px !important;  /* Fixed height */
#             border-radius: 25px !important; /* Rounded corners */
#             background-color: #009999 !important; /* Initial button color */
#             color: black !important;
#             font-size: 16px !important;
#             font-weight: bold !important;
            
#             border: none !important;
#             transition: background-color 0.3s ease-in-out;
#         }

#         /* Hover effect */
#         div.stButton > button:hover, div.stDownloadButton > button:hover {
#             background-color: red !important; /* Change to red on hover */
#             color: black !important;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

#     # Sidebar Navigation with Styled Buttons
#     st.sidebar.title("***Admin Panel***")
#     if "admin_page" not in st.session_state:
#         st.session_state["admin_page"] = "Upload Questions"

#     # Sidebar Buttons for Navigation
#     if st.sidebar.button("***Upload Questions***"):
#         st.session_state["admin_page"] = "Upload Questions"
#     if st.sidebar.button("***Add Questions***"):
#         st.session_state["admin_page"] = "Manually Add Questions"
#     if st.sidebar.button("***Manage Questions***"):
#         st.session_state["admin_page"] = "Manage Questions"
#     if st.sidebar.button("***Last Uploads***"):
#         st.session_state["admin_page"] = "Last Uploads"
#     if st.sidebar.button("***Sign Out***"):
#         logout()

#     # Upload Questions (File Upload)
#     if st.session_state["admin_page"] == "Upload Questions":
#         st.title("***Upload Questions via File***")
#         subject = st.text_input("Enter Subject Name:")
#         uploaded_file = st.file_uploader("Upload PDF/DOCX", type=["pdf", "docx"])
#         if st.button("***Process File***"):
#             if uploaded_file and subject.strip():
#                 file_path = os.path.join(UPLOADS_FOLDER, uploaded_file.name)
#                 with open(file_path, "wb") as f:
#                     f.write(uploaded_file.getbuffer())

#                 if uploaded_file.name.endswith(".pdf"):
#                     questions = extract_text_from_pdf(file_path)
#                 else:
#                     questions = extract_text_from_docx(file_path)

#                 if not questions:
#                     st.error("No questions found in the document. Please check formatting.")
#                     return

#                 dataset_path = save_to_dataset(subject, questions)
#                 store_upload_record(st.session_state["username"], subject, uploaded_file.name, dataset_path)
#                 st.success(f"Processed {len(questions)} questions and saved to {subject}.csv!")

#     # Manually Add Questions
#     elif st.session_state["admin_page"] == "Manually Add Questions":
#         st.title("***Manually Enter Questions***")
#         subject_manual = st.text_input("Enter Subject Name for Manual Entry:")
#         question_text = st.text_area("Enter Question:")
#         if st.button("***Add Question***"):
#             if subject_manual.strip() and question_text.strip():
#                 dataset_path = os.path.join(DATASET_FOLDER, f"{subject_manual}.csv")
#                 new_data = pd.DataFrame([{"question": question_text, "bloom_taxonomy_level": "Not Classified"}])

#                 if os.path.exists(dataset_path):
#                     df_existing = pd.read_csv(dataset_path)
#                     df_combined = pd.concat([df_existing, new_data], ignore_index=True)
#                 else:
#                     df_combined = new_data

#                 df_combined.to_csv(dataset_path, index=False)
#                 st.success(f"Question added to {subject_manual}.csv!")

#     # Manage Questions (Edit & Delete)
#     elif st.session_state["admin_page"] == "Manage Questions":
#         st.title("***Manage Last Uploaded Questions***")
#         datasets = [f for f in os.listdir(DATASET_FOLDER) if f.endswith(".csv")]
#         selected_dataset = st.selectbox("Select Subject Dataset", datasets)

#         if selected_dataset:
#             dataset_path = os.path.join(DATASET_FOLDER, selected_dataset)
#             df = pd.read_csv(dataset_path)
#             st.dataframe(df)

#             delete_question = st.text_input("Enter Question to Delete:")
#             if st.button("***Delete Question***"):
#                 df = df[df["question"] != delete_question]
#                 df.to_csv(dataset_path, index=False)
#                 st.success(f"Deleted question: {delete_question}")

#     # Last Uploads (View & Download)
#     elif st.session_state["admin_page"] == "Last Uploads":
#         st.title("Last Uploaded Files")
#         conn = sqlite3.connect(DB_PATH)
#         cursor = conn.cursor()
#         cursor.execute("SELECT admin, subject, file_name, dataset_path, uploaded_at FROM uploads ORDER BY uploaded_at DESC LIMIT 5")
#         uploads = cursor.fetchall()
#         conn.close()

#         if uploads:
#             for record in uploads:
#                 with st.container(border=True):
#                     st.write(f"**Subject:** {record[1]} | **File:** {record[2]} | **Date:** {record[4]}")
#                     col1,col2=st.columns(2)

#                     file_path = os.path.join(UPLOADS_FOLDER, record[2])
#                     dataset_path = record[3]
#                     with col1:
#                         if os.path.exists(file_path):
#                             with open(file_path, "rb") as file:
#                                 st.download_button(
#                                     label="***Download File***",
#                                     data=file,
#                                     file_name=record[2],
#                                     key=f"download_{record[2]}_{uuid.uuid4()}"
#                                 )
#                     with col2:
#                         if os.path.exists(dataset_path):
#                             if st.button(f"***View {record[1]} {record[4]} Dataset***"):
#                                 # df_uploaded = pd.read_csv(dataset_path)
#                                 # with col1:
#                                 #     st.write(df_uploaded.tail(len(df_uploaded)))
#                                 show_dataset(dataset_path)
#         else:
#             st.info("No uploads found.")

# def logout():
#     st.session_state["logged_in"] = False
#     st.rerun()
# import streamlit as st
# import os
# import pandas as pd
# import sqlite3
# import uuid
# from process_upload import extract_text_from_pdf, extract_text_from_docx, save_to_dataset, store_upload_record
# from classifier import classify_question  # Assuming this exists for Bloom's taxonomy classification

# DB_PATH = "new_database.db"
# DATASET_FOLDER = "dataset/"
# UPLOADS_FOLDER = "uploads/"

# os.makedirs(DATASET_FOLDER, exist_ok=True)
# os.makedirs(UPLOADS_FOLDER, exist_ok=True)

# DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]

# @st.dialog("Dataset Preview", width="large")
# def show_dataset(dataset_path):
#     df = pd.read_csv(dataset_path)
#     df = df.reset_index(drop=True)
#     df.index = df.index + 1
#     st.write(df.tail(len(df)))

# def show_admin_dashboard():
#     # CSS styling remains the same...
#     st.markdown(
#         """
#         <style>
#             div.stButton > button, div.stDownloadButton > button {
#                 width: 200px !important;
#                 height: 45px !important;
#                 border-radius: 25px !important;
#                 background-color: #009999 !important;
#                 color: black !important;
#                 font-size: 16px !important;
#                 font-weight: bold !important;
#                 border: none !important;
#                 transition: background-color 0.3s ease-in-out;
#             }

#             div.stButton > button:hover, div.stDownloadButton > button:hover {
#                 background-color: red !important;
#                 color: black !important;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

#     # Sidebar Navigation
#     st.sidebar.title("***Admin Panel***")
#     if "admin_page" not in st.session_state:
#         st.session_state["admin_page"] = "Upload Questions"

#     # Navigation buttons remain the same...
#     if st.sidebar.button("***Upload Questions***"):
#         st.session_state["admin_page"] = "Upload Questions"
#     if st.sidebar.button("***Add Questions***"):
#         st.session_state["admin_page"] = "Manually Add Questions"
#     if st.sidebar.button("***Manage Questions***"):
#         st.session_state["admin_page"] = "Manage Questions"
#     if st.sidebar.button("***Last Uploads***"):
#         st.session_state["admin_page"] = "Last Uploads"
#     if st.sidebar.button("***Sign Out***"):
#         logout()

#     # Upload Questions (File Upload)
#     if st.session_state["admin_page"] == "Upload Questions":
#         st.title("***Upload Questions via File***")
#         subject = st.text_input("Enter Subject Name:")
#         uploaded_file = st.file_uploader("Upload PDF/DOCX", type=["pdf", "docx"])
        
#         if st.button("***Process File***"):
#             if uploaded_file and subject.strip():
#                 try:
#                     file_path = os.path.join(UPLOADS_FOLDER, uploaded_file.name)
#                     with open(file_path, "wb") as f:
#                         print("file_path",file_path)
#                         f.write(uploaded_file.getbuffer())

#                     questions = []
#                     if uploaded_file.name.endswith(".pdf"):
#                         questions = extract_text_from_pdf(file_path)
#                     else:
#                         questions = extract_text_from_docx(file_path)

#                     if not questions:
#                         st.error("No questions found in the document. Please check formatting.")
#                         return

#                     # Classify each question
#                     print("questions",questions)
#                     classified_questions = []
#                     for q in questions:
#                         bloom_level = classify_question(q['question'])  # You'll need to implement this
#                         classified_questions.append({
#                             "question": q["question"],
#                             "bloom_taxonomy_level": bloom_level,
#                             "difficulty": q['difficulty']  # Default difficulty
#                         })

#                     dataset_path = save_to_dataset(subject, classified_questions)
#                     store_upload_record(st.session_state["username"], subject, uploaded_file.name, dataset_path)
#                     st.success(f"Processed {len(questions)} questions and saved to {subject}.csv!")
#                 except Exception as e:
#                     st.error(f"Error processing file: {str(e)}")

#     # Manually Add Questions
#     elif st.session_state["admin_page"] == "Manually Add Questions":
#         st.title("***Manually Enter Questions***")
#         subject_manual = st.text_input("Enter Subject Name for Manual Entry:")
#         question_text = st.text_area("Enter Question:")
#         difficulty = st.selectbox("Select Difficulty Level", DIFFICULTY_LEVELS)
        
#         if st.button("***Add Question***"):
#             if subject_manual.strip() and question_text.strip():
#                 try:
#                     dataset_path = os.path.join(DATASET_FOLDER, f"{subject_manual}.csv")
                    
#                     # Classify the question
#                     bloom_level = classify_question(question_text)
                    
#                     new_data = pd.DataFrame([{
#                         "question": question_text,
#                         "bloom_taxonomy_level": bloom_level,
#                         "difficulty": difficulty
#                     }])

#                     if os.path.exists(dataset_path):
#                         df_existing = pd.read_csv(dataset_path)
#                         df_combined = pd.concat([df_existing, new_data], ignore_index=True)
#                     else:
#                         df_combined = new_data

#                     df_combined.to_csv(dataset_path, index=False)
#                     st.success(f"Question added to {subject_manual}.csv!")
#                 except Exception as e:
#                     st.error(f"Error adding question: {str(e)}")

#     # Manage Questions (Edit & Delete)
#     elif st.session_state["admin_page"] == "Manage Questions":
#         st.title("***Manage Questions***")
#         datasets = [f for f in os.listdir(DATASET_FOLDER) if f.endswith(".csv")]
#         selected_dataset = st.selectbox("Select Subject Dataset", datasets)

#         if selected_dataset:
#             try:
#                 dataset_path = os.path.join(DATASET_FOLDER, selected_dataset)
#                 df = pd.read_csv(dataset_path)
                
#                 # Display questions with all attributes
#                 st.dataframe(df)

#                 # Question deletion with confirmation
#                 question_to_delete = st.selectbox("Select Question to Delete:", df['question'].tolist())
                
#                 if st.button("***Delete Selected Question***"):
#                     if question_to_delete:
#                         df = df[df["question"] != question_to_delete]
#                         df.to_csv(dataset_path, index=False)
#                         st.success(f"Deleted question: {question_to_delete}")
#                         st.rerun()  # Refresh the page to show updated dataset
#             except Exception as e:
#                 st.error(f"Error managing questions: {str(e)}")

#     # Last Uploads section remains mostly the same...
#     elif st.session_state["admin_page"] == "Last Uploads":
#         st.title("Last Uploaded Files")
#         try:
#             conn = sqlite3.connect(DB_PATH)
#             cursor = conn.cursor()
#             cursor.execute("""
#                 SELECT admin, subject, file_name, dataset_path, uploaded_at 
#                 FROM uploads 
#                 ORDER BY uploaded_at DESC 
#                 LIMIT 5
#             """)
#             uploads = cursor.fetchall()
#             conn.close()

#             if uploads:
#                 for record in uploads:
#                     with st.container(border=True):
#                         st.write(f"**Subject:** {record[1]} | **File:** {record[2]} | **Date:** {record[4]}")
#                         col1, col2 = st.columns(2)

#                         file_path = os.path.join(UPLOADS_FOLDER, record[2])
#                         dataset_path = record[3]
                        
#                         with col1:
#                             if os.path.exists(file_path):
#                                 with open(file_path, "rb") as file:
#                                     st.download_button(
#                                         label="***Download File***",
#                                         data=file,
#                                         file_name=record[2],
#                                         key=f"download_{record[2]}_{uuid.uuid4()}"
#                                     )
#                         with col2:
#                             if os.path.exists(dataset_path):
#                                 date=record[4].split(" ")
#                                 if st.button(f"***View {record[1]} {date[0]} Dataset***"):
#                                     show_dataset(dataset_path)
#             else:
#                 st.info("No uploads found.")
#         except Exception as e:
#             st.error(f"Error loading upload history: {str(e)}")

# def logout():
#     st.session_state["logged_in"] = False
#     st.rerun()

import streamlit as st # type: ignore
import os
import pandas as pd
import sqlite3
import uuid
from process_upload import extract_text_from_pdf, extract_text_from_docx, save_to_dataset, store_upload_record
from classifier import classify_question  
from auth import DB_PATH  
DB_PATH = "new_database.db"
DATASET_FOLDER = "dataset/"
UPLOADS_FOLDER = "uploads/"

os.makedirs(DATASET_FOLDER, exist_ok=True)
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]

@st.dialog("Dataset Preview", width="large")
def show_dataset(dataset_path):
    df = pd.read_csv(dataset_path)
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    st.write(df.tail(len(df)))

def show_admin_dashboard():
    # CSS styling remains the same...
    st.markdown(
        """
        <style>
            div.stButton > button, div.stDownloadButton > button {
                width: 200px !important;
                height: 45px !important;
                border-radius: 25px !important;
                background-color: #009999 !important;
                color: black !important;
                font-size: 16px !important;
                font-weight: bold !important;
                border: none !important;
                transition: background-color 0.3s ease-in-out;
            }

            div.stButton > button:hover, div.stDownloadButton > button:hover {
                background-color: red !important;
                color: black !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar Navigation
     # Adjust width as needed
    
    st.sidebar.title("***Admin Panel***")
    if "admin_page" not in st.session_state:
        st.session_state["admin_page"] = "Upload Questions"

    # Navigation buttons remain the same...
    if st.sidebar.button("***Upload Questions***"):
        st.session_state["admin_page"] = "Upload Questions"
    if st.sidebar.button("***Add Questions***"):
        st.session_state["admin_page"] = "Manually Add Questions"
    if st.sidebar.button("***Manage Questions***"):
        st.session_state["admin_page"] = "Manage Questions"
    if st.sidebar.button("***Last Uploads***"):
        st.session_state["admin_page"] = "Last Uploads"
    if st.sidebar.button("***Sign Out***"):
        logout()

    # Upload Questions (File Upload)
    if st.session_state["admin_page"] == "Upload Questions":
        st.title("***Upload Questions via File***")
        subject = st.text_input("Enter Subject Name:")
        uploaded_file = st.file_uploader("Upload PDF/DOCX", type=["pdf", "docx"])
        
        if st.button("***Process File***"):
            if uploaded_file and subject.strip():
                try:
                    file_path = os.path.join(UPLOADS_FOLDER, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        print("file_path",file_path)
                        f.write(uploaded_file.getbuffer())

                    questions = []
                    if uploaded_file.name.endswith(".pdf"):
                        questions = extract_text_from_pdf(file_path)
                    else:
                        questions = extract_text_from_docx(file_path)

                    if not questions:
                        st.error("No questions found in the document. Please check formatting.")
                        return

                    # Classify each question
                    print("questions",questions)
                    classified_questions = []
                    for q in questions:
                        bloom_level = classify_question(q['question'])  # You'll need to implement this
                        classified_questions.append({
                            "question": q["question"],
                            "bloom_taxonomy_level": bloom_level,
                            "difficulty": q['difficulty']  # Default difficulty
                        })

                    dataset_path = save_to_dataset(subject, classified_questions)
                    store_upload_record(st.session_state["username"], subject, uploaded_file.name, dataset_path)
                    st.success(f"Processed {len(questions)} questions and saved to {subject}.csv!")
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")

    # Manually Add Questions
    elif st.session_state["admin_page"] == "Manually Add Questions":
        st.title("***Manually Enter Questions***")
        subject_manual = st.text_input("Enter Subject Name for Manual Entry:")
        question_text = st.text_area("Enter Question:")
        difficulty = st.selectbox("Select Difficulty Level", DIFFICULTY_LEVELS)
        
        if st.button("***Add Question***"):
            if subject_manual.strip() and question_text.strip():
                try:
                    dataset_path = os.path.join(DATASET_FOLDER, f"{subject_manual}.csv")
                    
                    # Classify the question
                    bloom_level = classify_question(question_text)
                    
                    new_data = pd.DataFrame([{
                        "question": question_text,
                        "bloom_taxonomy_level": bloom_level,
                        "difficulty": difficulty
                    }])

                    if os.path.exists(dataset_path):
                        df_existing = pd.read_csv(dataset_path)
                        df_combined = pd.concat([df_existing, new_data], ignore_index=True)
                    else:
                        df_combined = new_data

                    df_combined.to_csv(dataset_path, index=False)
                    st.success(f"Question added to {subject_manual}.csv!")
                except Exception as e:
                    st.error(f"Error adding question: {str(e)}")

    # Manage Questions (Edit & Delete)
    elif st.session_state["admin_page"] == "Manage Questions":
        st.title("***Manage Questions***")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT admin, subject, file_name, dataset_path, uploaded_at 
            FROM uploads 
            WHERE admin = ?
            ORDER BY uploaded_at DESC
        """, (st.session_state["username"],))
        uploads = cursor.fetchall()
        conn.close()
        print("uploads",uploads[0][1])
        # datasets = [f for f in os.listdir(DATASET_FOLDER) if f.endswith(".csv")]
        datasets=[]
        for record in uploads:
            datasets.append(record[1]+".csv")
        selected_dataset = st.selectbox("Select Subject Dataset", datasets)
        print("selected_dataset",selected_dataset)
        if selected_dataset:
            try:
                dataset_path = os.path.join(DATASET_FOLDER, selected_dataset)
                df = pd.read_csv(dataset_path)
                
                # Display questions with all attributes
                st.dataframe(df)

                # Question deletion with confirmation
                question_to_delete = st.selectbox("Select Question to Delete:", df['question'].tolist())
                
                if st.button("***Delete Selected Question***"):
                    if question_to_delete:
                        df = df[df["question"] != question_to_delete]
                        df.to_csv(dataset_path, index=False)
                        st.success(f"Deleted question: {question_to_delete}")
                        st.rerun()  # Refresh the page to show updated dataset
            except Exception as e:
                st.error(f"Error managing questions: {str(e)}")

    # Last Uploads section remains mostly the same...
    # In admin_dashboard.py - Update Last Uploads section
    elif st.session_state["admin_page"] == "Last Uploads":
        st.title("Your Uploaded Files")
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT admin, subject, file_name, dataset_path, uploaded_at 
                FROM uploads 
                WHERE admin = ?
                ORDER BY uploaded_at DESC
            """, (st.session_state["username"],))
            uploads = cursor.fetchall()
            conn.close()

            if uploads:
                for record in uploads:
                    with st.container(border=True):
                        st.write(f"**Subject:** {record[1]} | **File:** {record[2]} | **Date:** {record[4]}")
                        col1, col2 = st.columns(2)

                        file_path = os.path.join(UPLOADS_FOLDER, record[2])
                        dataset_path = record[3]
                        
                        with col1:
                            if os.path.exists(file_path):
                                with open(file_path, "rb") as file:
                                    st.download_button(
                                        label="***Download File***",
                                        data=file,
                                        file_name=record[2],
                                        key=f"download_{record[2]}_{uuid.uuid4()}"
                                    )
                        with col2:
                            if os.path.exists(dataset_path):
                                date=record[4].split(" ")
                                if st.button(f"***View {record[1]} {date[0]} Dataset***"):
                                    show_dataset(dataset_path)
            else:
                st.info("You haven't uploaded any files yet.")
        except Exception as e:
            st.error(f"Error loading upload history: {str(e)}")
def logout():
    st.session_state["logged_in"] = False
    st.rerun()