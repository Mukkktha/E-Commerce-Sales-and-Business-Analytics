import pandas as pd
import numpy as np


def load_data(file_path):
    """Load and clean the e-commerce dataset."""

    df = pd.read_csv(file_path)

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"], errors="coerce"
    )

    # Handle missing values
    for column in ["City", "Payment_Method"]:
        if column in df.columns:
            df[column] = df[column].fillna("Unknown")

    # Remove duplicate records
    df = df.drop_duplicates(subset=["Order_ID"])

    # Create additional analytical columns
    df["Profit_Margin"] = np.where(
        df["Sales"] != 0,
        (df["Profit"] / df["Sales"]) * 100,
        0
    )

    df["Month"] = df["Order_Date"].dt.strftime("%Y-%m")
    df["Year"] = df["Order_Date"].dt.year

    return df


def calculate_kpis(df):
    """Calculate important business KPIs."""

    revenue = df["Sales"].sum()
    profit = df["Profit"].sum()

    return {
        "Total Revenue": round(revenue, 2),
        "Total Profit": round(profit, 2),
        "Total Orders": df["Order_ID"].nunique(),
        "Unique Customers": df["Customer_ID"].nunique(),
        "Profit Margin": round(
            (profit / revenue) * 100, 2
        ) if revenue else 0
    }


def monthly_sales_analysis(df):
    """Calculate monthly sales and profit."""

    result = (
        df.groupby("Month")
        .agg(
            Revenue=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique")
        )
        .reset_index()
        .sort_values("Month")
    )

    return result


def category_analysis(df):
    """Analyze product categories."""

    result = (
        df.groupby("Category")
        .agg(
            Revenue=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Units_Sold=("Quantity", "sum")
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    return result


def regional_analysis(df):
    """Analyze business performance by region."""

    result = (
        df.groupby("Region")
        .agg(
            Revenue=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique")
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    return result


def customer_analysis(df):
    """Analyze customer purchasing behaviour."""

    result = (
        df.groupby("Customer_ID")
        .agg(
            Total_Orders=("Order_ID", "nunique"),
            Total_Spending=("Sales", "sum"),
            Total_Profit=("Profit", "sum")
        )
        .reset_index()
    )

    result["Customer_Type"] = np.where(
        result["Total_Orders"] > 1,
        "Repeat Customer",
        "One-time Customer"
    )

    return result