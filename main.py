"""
main.py (FastAPI backend)

A simple API with 5 endpoints, one for each step of the project:
1. /upload     -> load the CSV and show a summary
2. /statistics -> show basic statistics
3. /ask        -> answer a natural language question
4. /chart      -> generate and return a chart image
5. /explain    -> explain what the chart shows

To run this file:
    uvicorn main:app --reload --port 8000
"""

import io
import pandas as pd
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from analysis import load_dataset, dataset_summary, basic_statistics, answer_question, explain_chart
from visualization import create_bar_chart, create_pie_chart

app = FastAPI(title="AI Data Analysis Assistant")

# Let the Streamlit frontend (running on a different address) call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# We keep the uploaded dataset in this simple global variable.
# This is fine for a single-user hackathon demo app.
current_dataset = None


class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "AI Data Analysis Assistant API is running. Go to /docs to try it."}


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """Step 1: Load the dataset and return a summary."""
    global current_dataset
    file_bytes = await file.read()
    current_dataset = pd.read_csv(io.BytesIO(file_bytes))
    return dataset_summary(current_dataset)


@app.get("/statistics")
def get_statistics():
    """Step 2: Return basic statistics about the dataset."""
    return basic_statistics(current_dataset)


@app.post("/ask")
def ask_question(request: Question):
    """Step 3: Answer a natural language question."""
    answer = answer_question(current_dataset, request.question)
    return {"answer": answer}


@app.get("/chart")
def get_chart(chart_type: str = "bar"):
    """Step 4: Generate a chart and return the image file."""
    if chart_type == "pie":
        chart_path = create_pie_chart(current_dataset)
    else:
        chart_path = create_bar_chart(current_dataset)
    return FileResponse(chart_path, media_type="image/png")


@app.get("/explain")
def get_explanation():
    """Step 5: Explain what the chart shows."""
    explanation = explain_chart(current_dataset)
    return {"explanation": explanation}
