#import streamlit as st
# from generate_paper import generate_question_paper

# st.title("📘 Bloom’s Taxonomy Question Paper Generator")
# subject = st.text_input("Enter subject name (CSV should exist in dataset/ folder)")
# num_questions = st.slider("Number of Questions", 1, 20, 5)
# total_marks = st.number_input("Total Marks", min_value=10, max_value=200, value=50)
# bloom_distribution = {
#     "Remember": 20,
#     "Understand": 20,
#     "Apply": 20,
#     "Analyze": 20,
#     "Evaluate": 10,
#     "Create": 10
# }
# difficulty_distribution = {
#     "easy": num_questions // 3,
#     "medium": num_questions // 3,
#     "hard": num_questions - 2 * (num_questions // 3)
# }
# marks_per_difficulty = {
#     "easy": 2,
#     "medium": 5,
#     "hard": 10
# }
# if st.button("Generate Question Paper"):
#     try:
#         file_path = generate_question_paper(
#             subject,
#             num_questions,
#             total_marks,
#             bloom_distribution,
#             difficulty_distribution,
#             marks_per_difficulty
#         )
#         st.success(f"Question paper generated: {file_path}")
#         with open(file_path, "rb") as f:
#             st.download_button(
#                 label="Download Question Paper",
#                 data=f,
#                 file_name=file_path.split("/")[-1],
#                 mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#             )

#     except Exception as e:
#         st.error(f"Error: {e}")



import streamlit as st
from generate_paper import generate_question_paper

st.title("📘 Question Paper Generator")
st.write("Generate exam question papers using Bloom’s Taxonomy.")

subject = st.text_input("Enter subject name (matches CSV file in dataset/):", "bloom_taxonomy_dataset")
num_questions = st.number_input("Number of Questions", min_value=1, max_value=50, value=5)
total_marks = st.number_input("Total Marks", min_value=10, max_value=200, value=50)

st.subheader("Bloom’s Taxonomy Distribution (%)")
bloom_distribution = {
    "Remembering": st.slider("Remembering (%)", 0, 100, 20),
    "Understanding": st.slider("Understanding (%)", 0, 100, 20),
    "Applying": st.slider("Applying (%)", 0, 100, 20),
    "Analyzing": st.slider("Analyzing (%)", 0, 100, 20),
    "Evaluating": st.slider("Evaluating (%)", 0, 100, 10),
    "Creating": st.slider("Creating (%)", 0, 100, 10),
}

total_percent = sum(bloom_distribution.values())
if total_percent != 100:
    st.warning(f"Percentages must add up to 100 (currently {total_percent}%).")

if st.button("Generate Question Paper"):
    if total_percent == 100:
        try:
            file_path = generate_question_paper(
                subject,
                num_questions,
                total_marks,
                bloom_distribution,
            )
            st.success(f"Question paper generated: {file_path}")
            with open(file_path, "rb") as f:
                st.download_button("⬇️ Download Question Paper", f, file_path)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Please adjust Bloom’s distribution so it adds up to 100.")




