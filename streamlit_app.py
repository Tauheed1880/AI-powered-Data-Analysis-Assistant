"""
streamlit_app.py

Frontend for the AI Data Analysis Assistant.
"""

import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="AI Data Analysis Assistant",
    page_icon="📊"
)

# Your deployed FastAPI backend
BACKEND_URL = "https://tauheed1880-fastapi-backend.hf.space"

st.title("📊 AI Data Analysis Assistant")

st.write(
    "Upload a CSV file, ask a question, generate a chart, and view an explanation."
)

uploaded_file = st.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)

if uploaded_file is not None:

    # -------------------------
    # Upload CSV
    # -------------------------

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "text/csv",
        )
    }

    upload_response = requests.post(
        f"{BACKEND_URL}/upload",
        files=files
    )

    if upload_response.status_code != 200:
        st.error("Unable to upload dataset.")
        st.stop()

    summary = upload_response.json()

    st.header("1️⃣ Dataset Summary")

    st.write(f"**Rows:** {summary['rows']}")
    st.write(f"**Columns:** {summary['columns']}")
    st.write("**Column Names:**", summary["column_names"])
    st.write("**Missing Values:**", summary["missing_values"])

    preview_df = pd.read_csv(uploaded_file)

    st.dataframe(preview_df.head())

    # -------------------------
    # Statistics
    # -------------------------

    st.header("2️⃣ Basic Statistics")

    stats_response = requests.get(
        f"{BACKEND_URL}/statistics"
    )

    if stats_response.status_code == 200:

        stats = stats_response.json()

        st.json(stats)

    else:

        st.error("Unable to fetch statistics.")

    # -------------------------
    # Question
    # -------------------------

    st.header("3️⃣ Ask a Question")

    st.caption(
        "Examples:\n"
        "- Which city has the maximum orders?\n"
        "- Which product has the highest sales?\n"
        "- Which region has the highest sales?\n"
        "- Which category is most frequent?"
    )

    question = st.text_input(
        "Enter your question"
    )

    chart_type = st.radio(
        "Chart Type",
        ["bar", "pie"],
        horizontal=True
    )

    if st.button("Get Answer"):

        if question.strip() == "":
            st.warning("Please enter a question.")
            st.stop()

        # -------------------------
        # Ask Question
        # -------------------------

        answer_response = requests.post(
            f"{BACKEND_URL}/ask",
            json={
                "question": question
            }
        )

        if answer_response.status_code == 200:

            answer = answer_response.json()

            st.success(answer["answer"])

        else:

            st.error("Unable to answer question.")
            st.stop()

        # -------------------------
        # Chart
        # -------------------------

        st.header("4️⃣ Visualization")

        chart_response = requests.get(
            f"{BACKEND_URL}/chart",
            params={
                "chart_type": chart_type
            }
        )

        if chart_response.status_code == 200:

            st.image(
                chart_response.content,
                use_container_width=True
            )

        else:

            st.error("Unable to generate chart.")

        # -------------------------
        # Explanation
        # -------------------------

        st.header("5️⃣ Explanation")

        explanation_response = requests.get(
            f"{BACKEND_URL}/explain"
        )

        if explanation_response.status_code == 200:

            explanation = explanation_response.json()

            st.info(
                explanation["explanation"]
            )

        else:

            st.error("Unable to generate explanation.")

else:

    st.info("Upload a CSV file to begin.")
