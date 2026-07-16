"""
visualization.py

Generate charts based on the user's question.
"""

import os
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

CHARTS_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "charts"
)
os.makedirs(CHARTS_FOLDER, exist_ok=True)

COLORS = [
    "#4C72B0",
    "#DD8452",
    "#55A868",
    "#C44E52",
    "#8172B2",
    "#937860",
    "#DA8BC3"
]


def create_bar_chart(df, question):
    """
    Create a bar chart according to the user's question.
    """

    q = question.lower()

    # -----------------------------
    # City with maximum orders
    # -----------------------------
    if "city" in q and "order" in q:

        grouped = (
            df.groupby("City")["Order ID"]
            .nunique()
            .sort_values(ascending=False)
        )

        title = "Orders by City"
        xlabel = "City"
        ylabel = "Number of Orders"

    # -----------------------------
    # Highest sales product
    # -----------------------------
    elif "product" in q:

        grouped = (
            df.groupby("Product Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        title = "Top 10 Products by Sales"
        xlabel = "Product"
        ylabel = "Sales"

    # -----------------------------
    # Highest sales region
    # -----------------------------
    elif "region" in q:

        grouped = (
            df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        title = "Sales by Region"
        xlabel = "Region"
        ylabel = "Sales"

    # -----------------------------
    # Most frequent category
    # -----------------------------
    elif "category" in q:

        grouped = (
            df["Category"]
            .value_counts()
        )

        title = "Category Frequency"
        xlabel = "Category"
        ylabel = "Count"

    # -----------------------------
    # Default chart
    # -----------------------------
    else:

        grouped = (
            df.groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        title = "Sales by Category"
        xlabel = "Category"
        ylabel = "Sales"

    plt.figure(figsize=(10, 5))

    plt.bar(
        grouped.index.astype(str),
        grouped.values,
        color="steelblue"
    )

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    save_path = os.path.join(
        CHARTS_FOLDER,
        "bar_chart.png"
    )

    plt.savefig(save_path)

    plt.close()

    return save_path


def create_pie_chart(df, question):
    """
    Create a pie chart according to the user's question.
    """

    q = question.lower()

    # City orders

    if "city" in q and "order" in q:

        grouped = (
            df.groupby("City")["Order ID"]
            .nunique()
            .sort_values(ascending=False)
        )

        title = "Orders by City"

    # Product sales

    elif "product" in q:

        grouped = (
            df.groupby("Product Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(8)
        )

        title = "Top Products by Sales"

    # Region sales

    elif "region" in q:

        grouped = (
            df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        title = "Sales by Region"

    # Category frequency

    elif "category" in q:

        grouped = df["Category"].value_counts()

        title = "Category Frequency"

    # Default

    else:

        grouped = (
            df.groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        title = "Sales by Category"

    plt.figure(figsize=(7, 7))

    plt.pie(
        grouped.values,
        labels=grouped.index,
        autopct="%1.1f%%",
    )

    plt.title(title)

    plt.tight_layout()

    save_path = os.path.join(
        CHARTS_FOLDER,
        "pie_chart.png"
    )

    plt.savefig(save_path)

    plt.close()

    return save_path
