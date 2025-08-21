import streamlit as st
st.title("Bloom’s Taxonomy Question Generator")
subject = st.text_input("Enter subject name")
bloom_level = st.selectbox("Select Bloom’s Level",["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"])
num_questions = st.slider("Number of Questions",1,20,5)
if st.button("Generate Paper"):
    questions = [f"Sample question {i+1} for {subject} ({bloom_level})" for i in range(num_questions)]
    
    st.success("✅ Generated Question Paper")
    for i, q in enumerate(questions, 1):
        st.write(f"**Q{i}:** {q}")
