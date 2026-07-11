"""
visualization.py

Simple chart-drawing functions using Matplotlib.
Charts are saved as PNG files inside the charts/ folder.
"""

import os
import matplotlib
matplotlib.use("Agg")  # lets matplotlib run without a screen (needed on servers)
import matplotlib.pyplot as plt

# folder where charts get saved (../charts, next to backend/)
CHARTS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "charts")
os.makedirs(CHARTS_FOLDER, exist_ok=True)

COLORS = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2"]


def create_bar_chart(df):
    """Bar chart: total Sales for each Category."""
    grouped = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)

    plt.figure(figsize=(8, 5))
    plt.bar(grouped.index, grouped.values, color=COLORS[: len(grouped)])
    plt.title("Total Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Sales")
    plt.tight_layout()

    save_path = os.path.join(CHARTS_FOLDER, "bar_chart.png")
    plt.savefig(save_path)
    plt.close()
    return save_path


def create_pie_chart(df):
    """Pie chart: how many records belong to each Category."""
    counts = df["Category"].value_counts()

    plt.figure(figsize=(6, 6))
    plt.pie(counts.values, labels=counts.index, autopct="%1.1f%%", colors=COLORS[: len(counts)])
    plt.title("Category Distribution")
    plt.tight_layout()

    save_path = os.path.join(CHARTS_FOLDER, "pie_chart.png")
    plt.savefig(save_path)
    plt.close()
    return save_path
