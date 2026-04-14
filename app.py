import streamlit as st
import docx
import PyPDF2
import re

# ---------------- CLEAN TEXT ----------------
def cleanResume(txt):
    txt = re.sub('http\S+\s', ' ', txt)
    txt = re.sub('RT|cc', ' ', txt)
    txt = re.sub('#\S+\s', ' ', txt)
    txt = re.sub('@\S+', ' ', txt)
    txt = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', txt)
    txt = re.sub(r'[^\x00-\x7f]', ' ', txt)
    txt = re.sub('\s+', ' ', txt)
    return txt

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

# ---------------- RULE-BASED PREDICTION ----------------
def predict_category(text):
    text = text.lower()

    if "machine learning" in text or "data science" in text:
        return "Data Science"
    elif "html" in text or "css" in text or "javascript" in text:
        return "Web Developer"
    elif "java" in text or "spring" in text:
        return "Backend Developer"
    elif "c++" in text or "dsa" in text:
        return "Software Developer"
    else:
        return "General Role"

# ---------------- SKILLS ----------------
skills_db = [
    "python", "java", "c++", "machine learning",
    "html", "css", "javascript", "react",
    "node", "sql", "mongodb"
]

def extract_skills(text):
    found = []
    for skill in skills_db:
        if skill in text.lower():
            found.append(skill)
    return list(set(found))

# ---------------- JOB MATCH ----------------
job_roles = {
    "Data Science": ["python", "machine learning"],
    "Web Developer": ["html", "css", "javascript"],
    "Backend Developer": ["java", "sql"],
    "Software Developer": ["c++", "dsa"]
}

def match_jobs(user_skills):
    matched = []
    for job, skills in job_roles.items():
        if any(skill in user_skills for skill in skills):
            matched.append(job)
    return matched

# ---------------- SCORE ----------------
def calculate_score(skills):
    return min(len(skills) * 10, 100)

# ---------------- UI ----------------
def main():
    st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

    st.title("AI Resume Analyzer & Job Matcher")
    st.markdown("Upload your resume and get instant insights!")

    uploaded_file = st.file_uploader("📤 Upload Resume", type=["pdf", "docx", "txt"])

    if uploaded_file:
        with st.spinner("Analyzing your resume..."):
            text = handle_file(uploaded_file)

            if text:
                text = cleanResume(text)

                category = predict_category(text)
                skills = extract_skills(text)
                jobs = match_jobs(skills)
                score = calculate_score(skills)

                tab1, tab2, tab3 = st.tabs(["📄 Resume", "📊 Analysis", "💼 Job Match"])

                # TAB 1
                with tab1:
                    st.text_area("Extracted Resume Text", text, height=300)

                # TAB 2
                with tab2:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("🎯 Predicted Role", category)
                        st.metric("📊 ATS Score", f"{score}/100")

                    with col2:
                        st.write("### 🛠 Skills Found")
                        if skills:
                            for s in skills:
                                st.write(f"✔️ {s}")
                        else:
                            st.write("No skills detected")

                # TAB 3
                with tab3:
                    st.write("### 💼 Recommended Jobs")
                    if jobs:
                        for job in jobs:
                            st.success(job)
                    else:
                        st.warning("No matching jobs found")

if __name__ == "__main__":
    main()
