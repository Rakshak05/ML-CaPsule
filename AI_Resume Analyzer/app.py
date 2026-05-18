import streamlit as st
import pdfplumber
from skills import skills_list

# Function to extract text from PDF
def extract_text(pdf_file):
    text = ""
    
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    
    return text.lower()

# Function to find skills
def analyze_resume(text):
    found_skills = []
    
    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)
    
    return found_skills

# Streamlit UI
st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

if uploaded_file:
    resume_text = extract_text(uploaded_file)
    
    skills_found = analyze_resume(resume_text)
    
    st.subheader("Detected Skills")
    
    if skills_found:
        for skill in skills_found:
            st.write("✅", skill)
    else:
        st.write("No matching skills found.")
    
    score = len(skills_found) * 10
    
    st.subheader("Resume Score")
    st.write(f"{score}/100")
    
    if score < 50:
        st.warning("Add more technical skills to improve your resume.")
    else:
        st.success("Good resume profile!")