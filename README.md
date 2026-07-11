# 📊 AI Data Analysis Assistant

A simple AI-powered assistant that reads a CSV dataset, answers questions
about it in plain English, draws a chart, and explains what the chart shows.

- **Frontend:** Streamlit (`streamlit_app.py`)
- **Backend:** FastAPI (`backend/main.py`)
- **Notebook:** `notebook.ipynb` — the same steps, one cell at a time

## Project Structure

```
project/
├── streamlit_app.py       # Streamlit frontend
├── backend/
│   ├── main.py             # FastAPI backend (the API)
│   ├── analysis.py         # Loads data, calculates stats, answers questions
│   ├── visualization.py    # Draws the charts
│   └── Dockerfile          # For deploying the backend to Hugging Face
├── notebook.ipynb          # Steps explained cell by cell
├── dataset.csv              # Sample dataset (Superstore sales data)
├── requirements.txt         # All required libraries
├── charts/                  # Generated chart images are saved here
└── README.md
```

## How It Works (in plain terms)

1. **Load Dataset** – `analysis.load_dataset()` reads the CSV with pandas.
2. **Analyze the Dataset** – `analysis.basic_statistics()` calculates total,
   average, max, and min sales, and counts orders and products.
3. **Answer Questions** – `analysis.answer_question()` looks for keywords
   in your question (like "highest", "average", "city", "category") and
   runs the matching pandas calculation. No complicated NLP — just simple
   keyword matching.
4. **Generate a Chart** – `visualization.py` uses Matplotlib to draw a bar
   chart or pie chart of sales by category.
5. **Explain the Result** – `analysis.explain_chart()` writes one simple
   sentence about the chart. If you set an `ANTHROPIC_API_KEY`, it asks
   Claude to make that sentence sound friendlier — but it works fine
   without an API key too.

## Running It Locally

**1. Install everything:**
```bash
pip install -r requirements.txt
```

**2. Start the backend** (in one terminal):
```bash
cd backend
uvicorn main:app --reload --port 8000
```
Open `http://localhost:8000/docs` to see and test the API directly.

**3. Start the frontend** (in a second terminal):
```bash
streamlit run streamlit_app.py
```
This opens the web app in your browser. It talks to the backend at
`http://localhost:8000` (you can change this at the top of `streamlit_app.py`).

**4. (Optional) Add a Claude API key** for friendlier explanations:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```
The app works fine without this — it just uses a simpler sentence instead.

**5. Try the notebook:**
```bash
jupyter notebook notebook.ipynb
```
Run the cells from top to bottom. It reads `dataset.csv` from the same folder.

## Deploying It

### Backend → Hugging Face Spaces
1. Create a new Space, choose **Docker** as the SDK.
2. Upload everything inside the `backend/` folder (it already has a
   `Dockerfile` and `requirements.txt`).
3. (Optional) Add `ANTHROPIC_API_KEY` as a Space secret.
4. Your backend will be live at something like
   `https://your-username-your-space.hf.space`.

### Frontend → streamlit.io (Streamlit Community Cloud)
1. Push this project to GitHub.
2. On streamlit.io, create a new app pointing to `streamlit_app.py`.
3. In `streamlit_app.py`, change the `BACKEND_URL` variable at the top to
   your Hugging Face Space URL from the step above.
4. Deploy!

## Example Questions to Try

- "Which product has the highest sales?"
- "What is the average sales?"
- "Which city has the maximum orders?"
- "Which category is most frequent?"
- "What is the total sales?"
- "Which region has the highest sales?"
