import streamlit as st
import docx
import PyPDF2
import re

# ---------------- FILE HANDLING ----------------
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ''
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text

def extract_text_from_txt(file):
    try:
        return file.read().decode('utf-8')
    except:
        return file.read().decode('latin-1')

def handle_file(uploaded_file):
    ext = uploaded_file.name.split('.')[-1].lower()
    if ext == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    elif ext == 'docx':
        return extract_text_from_docx(uploaded_file)
    elif ext == 'txt':
        return extract_text_from_txt(uploaded_file)
    else:
        return None

# ---------------- RULE-BASED CATEGORY ----------------
def predict_category(text):
    text = text.lower()
    if "machine learning" in text or "data science" in text:
        return "Data Science"
    elif "html" in text or "css" in text or "javascript" in text:
        return "Web Developer"
    elif "java" in text or "spring" in text:
        return "Backend Developer"
    else:
        return "General Role"

# ---------------- SKILLS ----------------
skills_db = ["python", "java", "c++", "html", "css", "javascript", "react", "sql"]

def extract_skills(text):
    return [s for s in skills_db if s in text.lower()]

# ---------------- SCORE ----------------
def calculate_score(skills):
    return min(len(skills) * 10, 100)

# ---------------- UI ----------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🚀 AI Resume Analyzer & Job Matcher")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

if uploaded_file:
    text = handle_file(uploaded_file)

    if text:
        category = predict_category(text)
        skills = extract_skills(text)
        score = calculate_score(skills)

        tab1, tab2 = st.tabs(["📄 Resume", "📊 Analysis"])

        with tab1:
            st.text_area("Resume Content", text, height=300)

        with tab2:
            st.metric("🎯 Role", category)
            st.metric("📊 ATS Score", f"{score}/100")

            st.write("### Skills Found")
            for s in skills:
                st.write(f"✔️ {s}")
