import streamlit as st
import fitz  # PyMuPDF
import openai
import os

st.set_page_config(page_title="Chatbot Tài chính", layout="centered")
st.title("🤖 Chatbot Phân tích Báo cáo Tài chính")
st.markdown("Tải lên báo cáo tài chính (.PDF) và đặt câu hỏi bằng tiếng Việt.")

api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else st.text_input("Nhập OpenAI API Key", type="password")
uploaded_file = st.file_uploader("📄 Tải lên file PDF", type="pdf")

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if uploaded_file and api_key:
    text = extract_text_from_pdf(uploaded_file)
    question = st.text_input("💬 Đặt câu hỏi về báo cáo tài chính")

    if question:
        with st.spinner("Đang phân tích..."):
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Bạn là một chuyên gia phân tích tài chính, hãy trả lời ngắn gọn và chính xác."},
                    {"role": "user", "content": f"Báo cáo tài chính:
{text}

Câu hỏi: {question}"}
                ],
                temperature=0.5
            )
            st.success(response["choices"][0]["message"]["content"])