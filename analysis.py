"""
analysis.py

Simple functions to load the dataset, calculate statistics,
and answer natural language questions.

This file is written specifically for our dataset, which has these
important columns: Sales, Category, City, Order ID, Product Name, Region.
"""

import os
import pandas as pd


def load_dataset(path):
    """Read the CSV file into a pandas DataFrame."""
    df = pd.read_csv(path)
    return df


def dataset_summary(df):
    """Return basic information about the dataset."""
    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.astype(str).to_dict(),
    }
    return summary


def basic_statistics(df):
    """Calculate a few simple, useful statistics about the dataset."""
    stats = {
        "total_sales": round(df["Sales"].sum(), 2),
        "average_sales": round(df["Sales"].mean(), 2),
        "max_sales": round(df["Sales"].max(), 2),
        "min_sales": round(df["Sales"].min(), 2),
        "total_orders": df["Order ID"].nunique(),
        "total_products": df["Product Name"].nunique(),
    }
    return stats


def answer_question(df, question):
    """
    Answer a natural language question about the dataset.

    This uses simple if/elif checks: we look for keywords in the
    question and run the matching pandas calculation.
    """
    q = question.lower()

    # Which product generated the highest sales?
    if "product" in q and ("highest" in q or "top" in q or "most" in q):
        grouped = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False)
        top_product = grouped.index[0]
        top_value = grouped.iloc[0]
        return f"'{top_product}' has the highest sales, with a total of {top_value:,.2f}."

    # What is the average sales value?
    if "average" in q and "sales" in q:
        avg_value = df["Sales"].mean()
        return f"The average sales value is {avg_value:,.2f}."

    # Which city has the maximum orders?
    if "city" in q and "order" in q:
        grouped = df.groupby("City")["Order ID"].nunique().sort_values(ascending=False)
        top_city = grouped.index[0]
        top_value = grouped.iloc[0]
        return f"'{top_city}' has the maximum number of orders: {top_value}."

    # Which category appears most frequently?
    if "category" in q and ("frequent" in q or "most" in q or "common" in q):
        counts = df["Category"].value_counts()
        top_category = counts.index[0]
        top_value = counts.iloc[0]
        return f"'{top_category}' is the most frequent category, appearing {top_value} times."

    # What is the total sales?
    if "total" in q and "sales" in q:
        total_value = df["Sales"].sum()
        return f"The total sales amount is {total_value:,.2f}."

    # Which region has the highest sales?
    if "region" in q and ("highest" in q or "top" in q or "most" in q):
        grouped = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
        top_region = grouped.index[0]
        top_value = grouped.iloc[0]
        return f"'{top_region}' region has the highest sales, with a total of {top_value:,.2f}."

    # Default answer if we don't recognize the question
    return (
        "I can answer questions about: highest sales product, average sales, "
        "city with maximum orders, most frequent category, total sales, "
        "and region with highest sales. Please try one of those."
    )


def explain_chart(df):
    """
    Create a short, simple explanation of the bar chart
    (total sales by category).

    If an ANTHROPIC_API_KEY is set, we ask Claude to rephrase the
    explanation in a friendlier way. Otherwise, we just use our
    own simple sentence. Either way, this function never crashes.
    """
    grouped = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    top_category = grouped.index[0]
    top_value = grouped.iloc[0]
    percentage = (top_value / grouped.sum()) * 100

    simple_explanation = (
        f"The {top_category} category contributes the highest sales, "
        f"accounting for approximately {percentage:.1f}% of total sales."
    )

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return simple_explanation

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": f"Rewrite this in one simple, friendly sentence: {simple_explanation}"
            }],
        )
        return response.content[0].text.strip()
    except Exception:
        # If the API call fails for any reason, just use the simple version
        return simple_explanation
