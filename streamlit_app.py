import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

# Show title and description.
st.title("📄 Cover Letter LLM")
st.write(
    "Upload your resume and paste a job description to generate an awesome cover letter! "
    "To use this app, you need to provide an API key (also model name and base url in some cases) compatible with OpenAI SDK. "
)

api_key = st.text_input("API Key", type="password")
base_url = st.text_input("Base URL", help="For proxy or hosted model")
model_name = st.text_input("Model Name", help="Please refer to the model provider for exact model name")


# Create an OpenAI client.
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
    "Upload your resume (.pdf)", type=("pdf")
)

if uploaded_file:
    text = ""
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        text = text + page.extract_text(extraction_mode="layout")
    st.write(text)

# Ask the user for a text input via `st.text_area`.
description = st.text_area(
    "Now paste the job description here",
    disabled=not uploaded_file,
)

if st.button("Submit"):
    submitted = True

if uploaded_file and description and submitted:

    messages = [
        {
            "role": "system",
            "content": "You are an expert in writing cover letter. You can write very high quality cover letters if a resume and a job description are provided to you. The cover letter written by you should impress the recruiter."
        },
        {
            "role": "user",
            "content": f"Here's a resume: {text} \n\n---\n\n and here's a job description: {description} \n\n---\n\n Now write a cover letter for the person mntioned in the resume for job",
        }
    ]

    # Generate an answer using the OpenAI API.
    completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=True,
    )

    # Stream the response to the app using `st.write_stream`.
    st.write_stream(completion)
