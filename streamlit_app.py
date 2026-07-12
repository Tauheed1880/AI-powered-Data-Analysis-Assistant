"""
streamlit_app.py

Simple frontend for the AI Data Analysis Assistant.
This app talks to the FastAPI backend (main.py) over HTTP.

To run this file (after starting the backend):
    streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="AI Data Analysis Assistant", page_icon="📊")

# Change this to your deployed backend URL when you deploy to Hugging Face
BACKEND_URL = "https://tauheed1880-fastapi-backend.hf.space"

st.title("AI Data Analysis Assistant")
st.write("Upload a CSV file to get a summary, ask questions, see a chart, and get an explanation.")

uploaded_file = st.file_uploader("Upload your CSV dataset", type=["csv"])

if uploaded_file is not None:

    # --- Step 1: Upload the file to the backend and show the summary ---
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
    response = requests.post(f"{BACKEND_URL}/upload", files=files)
    summary = response.json()

    st.header("1Dataset Summary")
    st.write(f"**Rows:** {summary['rows']}")
    st.write(f"**Columns:** {summary['columns']}")
    st.write("**Column names:**", summary["column_names"])
    st.write("**Missing values:**", summary["missing_values"])

    preview_df = pd.read_csv(uploaded_file)
    st.dataframe(preview_df.head())

    # --- Step 2: Show basic statistics ---
    st.header("2️Basic Statistics")
    stats = requests.get(f"{BACKEND_URL}/statistics").json()
    st.write(stats)

    # --- Step 3: Ask a question ---
    st.header("3️Ask a Question")
    st.caption(
        "Try: 'Which product has the highest sales?', 'What is the average sales?', "
        "'Which city has the maximum orders?', 'Which category is most frequent?'"
    )
    question = st.text_input("Type your question here:")

    if st.button("Get Answer") and question.strip():
        result = requests.post(f"{BACKEND_URL}/ask", json={"question": question})
        st.success(result.json()["answer"])

    # --- Step 4: Generate a chart ---
    st.header("4️Chart")
    chart_type = st.radio("Choose chart type:", ["bar", "pie"], horizontal=True)

    if st.button("Generate Chart"):
        chart_response = requests.get(f"{BACKEND_URL}/chart", params={"chart_type": chart_type})
        st.image(chart_response.content)

        # --- Step 5: Explain the chart ---
        st.header("Explanation")
        explanation = requests.get(f"{BACKEND_URL}/explain").json()
        st.info(explanation["explanation"])

else:
    st.info(" Upload a CSV file to get started.")
