"""
analysis.py

Functions to load the dataset, calculate statistics,
answer natural language questions, and explain charts.
"""

import os
import pandas as pd


def load_dataset(path):
    """Read the CSV file into a pandas DataFrame."""
    return pd.read_csv(path)


def dataset_summary(df):
    """Return basic information about the dataset."""
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.astype(str).to_dict(),
    }


def basic_statistics(df):
    """Calculate useful statistics."""
    return {
        "total_sales": round(df["Sales"].sum(), 2),
        "average_sales": round(df["Sales"].mean(), 2),
        "max_sales": round(df["Sales"].max(), 2),
        "min_sales": round(df["Sales"].min(), 2),
        "total_orders": df["Order ID"].nunique(),
        "total_products": df["Product Name"].nunique(),
    }


def answer_question(df, question):
    q = question.lower()

    # Highest Sales Product
    if "product" in q and ("highest" in q or "top" in q or "most" in q):
        grouped = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False)
        return (
            f"'{grouped.index[0]}' has the highest sales "
            f"with a total of {grouped.iloc[0]:,.2f}."
        )

    # Average Sales
    elif "average" in q and "sales" in q:
        return f"The average sales value is {df['Sales'].mean():,.2f}."

    # Maximum Orders by City
    elif "city" in q and "order" in q:
        grouped = df.groupby("City")["Order ID"].nunique().sort_values(ascending=False)
        return (
            f"'{grouped.index[0]}' has the maximum number of orders "
            f"({grouped.iloc[0]} orders)."
        )

    # Most Frequent Category
    elif "category" in q and ("frequent" in q or "most" in q or "common" in q):
        counts = df["Category"].value_counts()
        return (
            f"'{counts.index[0]}' is the most frequent category "
            f"with {counts.iloc[0]} records."
        )

    # Total Sales
    elif "total" in q and "sales" in q:
        return f"The total sales amount is {df['Sales'].sum():,.2f}."

    # Highest Sales Region
    elif "region" in q and ("highest" in q or "top" in q or "most" in q):
        grouped = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
        return (
            f"'{grouped.index[0]}' region has the highest sales "
            f"with a total of {grouped.iloc[0]:,.2f}."
        )

    return (
        "I can answer questions about highest sales product, "
        "average sales, city with maximum orders, "
        "most frequent category, total sales, "
        "and highest sales region."
    )


def explain_chart(df, question):
    """
    Explain the generated chart according to the user's question.
    """

    q = question.lower()

    if "city" in q and "order" in q:
        grouped = df.groupby("City")["Order ID"].nunique().sort_values(ascending=False)
        return (
            f"The chart shows the number of orders for each city. "
            f"{grouped.index[0]} has the highest number of orders "
            f"({grouped.iloc[0]} orders)."
        )

    elif "product" in q:
        grouped = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False)
        return (
            f"The chart compares total sales by product. "
            f"{grouped.index[0]} generated the highest sales "
            f"({grouped.iloc[0]:,.2f})."
        )

    elif "region" in q:
        grouped = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
        return (
            f"The chart compares sales across regions. "
            f"{grouped.index[0]} region generated the highest sales "
            f"({grouped.iloc[0]:,.2f})."
        )

    elif "category" in q:
        counts = df["Category"].value_counts()
        return (
            f"The chart shows how frequently each category appears. "
            f"{counts.index[0]} is the most common category "
            f"with {counts.iloc[0]} records."
        )

    else:
        grouped = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)

        percentage = grouped.iloc[0] / grouped.sum() * 100

        return (
            f"The chart compares total sales by category. "
            f"{grouped.index[0]} contributes the highest sales "
            f"({percentage:.1f}% of total sales)."
        )
