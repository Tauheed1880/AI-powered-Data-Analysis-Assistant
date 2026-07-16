import io
import pandas as pd

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from analysis import (
    dataset_summary,
    basic_statistics,
    answer_question,
    explain_chart,
)

from visualization import (
    create_bar_chart,
    create_pie_chart,
)

app = FastAPI(title="AI Data Analysis Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store uploaded dataset
current_dataset = None

# Store the user's latest question
current_question = ""


class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "AI Data Analysis Assistant API is running."}


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    global current_dataset

    file_bytes = await file.read()

    current_dataset = pd.read_csv(io.BytesIO(file_bytes))

    return dataset_summary(current_dataset)


@app.get("/statistics")
def get_statistics():

    if current_dataset is None:
        return {"error": "Please upload a dataset first."}

    return basic_statistics(current_dataset)


@app.post("/ask")
def ask_question(request: Question):

    global current_question

    if current_dataset is None:
        return {"answer": "Please upload a dataset first."}
    current_question = request.question
    answer = answer_question(current_dataset, request.question)

    return {"answer": answer}


@app.get("/chart")
def get_chart(chart_type: str = "bar"):

    if current_dataset is None:
        return {"error": "Please upload a dataset first."}

    if chart_type == "pie":
        chart = create_pie_chart(
            current_dataset,
            current_question,
        )
    else:
        chart = create_bar_chart(
            current_dataset,
            current_question,
        )

    return FileResponse(
        chart,
        media_type="image/png",
    )


@app.get("/explain")
def get_explanation():

    if current_dataset is None:
        return {"error": "Please upload a dataset first."}

    explanation = explain_chart(
        current_dataset,
        current_question,
    )

    return {
        "explanation": explanation
    }
