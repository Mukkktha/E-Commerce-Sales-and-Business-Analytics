import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path

from src.analysis import (
    load_data,
    calculate_kpis,
    monthly_sales_analysis,
    category_analysis,
    regional_analysis,
    customer_analysis
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("🛒 E-Commerce Sales & Business Analytics")
st.caption(
    "Interactive Business Intelligence Dashboard | Python | SQL | Streamlit"
)

# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

BASE_DIR = Path(__file__).parent

possible_paths = [
    BASE_DIR / "data" / "ecommerce_orders.csv",
    BASE_DIR / "DATA" / "ecommerce_orders.csv"
]

DATA_PATH = next(
    (path for path in possible_paths if path.exists()),
    None
)

if DATA_PATH is None:
    st.error(
        "Dataset not found! Please check that "
        "ecommerce_orders.csv is inside your data or DATA folder."
    )
    st.stop()


@st.cache_data
def get_data(file_path):
    return load_data(file_path)


df = get_data(DATA_PATH)

if df.empty:
    st.error("The dataset is empty.")
    st.stop()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("🎛️ Dashboard Filters")

min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

selected_regions = st.sidebar.multiselect(
    "Select Region",
    sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    sorted(df["Category"].dropna().unique()),
    default=sorted(df["Category"].dropna().unique())
)

selected_channels = st.sidebar.multiselect(
    "Select Sales Channel",
    sorted(df["Sales_Channel"].dropna().unique()),
    default=sorted(df["Sales_Channel"].dropna().unique())
)

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered = filtered[
        (filtered["Order_Date"].dt.date >= start_date) &
        (filtered["Order_Date"].dt.date <= end_date)
    ]

filtered = filtered[
    filtered["Region"].isin(selected_regions) &
    filtered["Category"].isin(selected_categories) &
    filtered["Sales_Channel"].isin(selected_channels)
]

if filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# --------------------------------------------------
# BUSINESS PERFORMANCE KPIs
# --------------------------------------------------

kpis = calculate_kpis(filtered)

st.subheader("📈 Business Performance Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Revenue",
    f"₹{kpis['Total Revenue']:,.0f}"
)

col2.metric(
    "Total Profit",
    f"₹{kpis['Total Profit']:,.0f}"
)

col3.metric(
    "Total Orders",
    f"{kpis['Total Orders']:,}"
)

col4.metric(
    "Unique Customers",
    f"{kpis['Unique Customers']:,}"
)

col5.metric(
    "Profit Margin",
    f"{kpis['Profit Margin']:.2f}%"
)

st.divider()

# --------------------------------------------------
# DASHBOARD TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Sales Overview",
    "📦 Product Analysis",
    "🌍 Regional Analysis",
    "👥 Customer Analysis",
    "📋 Data Explorer"
])

# --------------------------------------------------
# TAB 1: SALES OVERVIEW
# --------------------------------------------------

with tab1:

    st.subheader("Monthly Sales and Profit Trends")

    monthly = monthly_sales_analysis(filtered)

    fig = px.line(
        monthly,
        x="Month",
        y=["Revenue", "Profit"],
        markers=True,
        title="Monthly Revenue and Profit"
    )

    fig.update_layout(
        legend_title_text="Metric",
        xaxis_title="Month",
        yaxis_title="Amount (₹)"
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:

        channel_data = (
            filtered.groupby("Sales_Channel")["Sales"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            channel_data,
            names="Sales_Channel",
            values="Sales",
            hole=0.45,
            title="Revenue by Sales Channel"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        status_data = (
            filtered["Order_Status"]
            .value_counts()
            .rename_axis("Order_Status")
            .reset_index(name="Orders")
        )

        fig = px.bar(
            status_data,
            x="Order_Status",
            y="Orders",
            title="Order Status Distribution",
            text_auto=True
        )

        st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# TAB 2: PRODUCT ANALYSIS
# --------------------------------------------------

with tab2:

    st.subheader("Product and Category Performance")

    category_data = category_analysis(filtered)

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            category_data,
            x="Category",
            y="Revenue",
            title="Revenue by Category",
            text_auto=".2s"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.bar(
            category_data,
            x="Category",
            y="Profit",
            title="Profit by Category",
            text_auto=".2s"
        )

        st.plotly_chart(fig, use_container_width=True)

    top_products = (
        filtered.groupby("Product")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_products,
        x="Sales",
        y="Product",
        orientation="h",
        title="Top 10 Products by Revenue",
        text_auto=".2s"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Category Performance Details")

    st.dataframe(
        category_data,
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# TAB 3: REGIONAL ANALYSIS
# --------------------------------------------------

with tab3:

    st.subheader("Regional Business Performance")

    region_data = regional_analysis(filtered)

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            region_data,
            x="Region",
            y="Revenue",
            title="Revenue by Region",
            text_auto=".2s"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.bar(
            region_data,
            x="Region",
            y="Profit",
            title="Profit by Region",
            text_auto=".2s"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Regional Performance Details")

    st.dataframe(
        region_data,
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# TAB 4: CUSTOMER ANALYSIS
# --------------------------------------------------

with tab4:

    st.subheader("Customer Purchasing Behaviour")

    customers = customer_analysis(filtered)

    customer_types = (
        customers.groupby("Customer_Type")
        .size()
        .reset_index(name="Customers")
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            customer_types,
            names="Customer_Type",
            values="Customers",
            hole=0.45,
            title="Repeat vs One-Time Customers"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.histogram(
            customers,
            x="Total_Orders",
            nbins=15,
            title="Customer Order Frequency"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 10 Customers")

    top_customers = (
        customers.sort_values(
            "Total_Spending",
            ascending=False
        ).head(10)
    )

    st.dataframe(
        top_customers,
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# TAB 5: DATA EXPLORER
# --------------------------------------------------

with tab5:

    st.subheader("Explore Order-Level Data")

    st.write(
        f"Total records available: {len(filtered):,}"
    )

    st.dataframe(
        filtered.sort_values(
            "Order_Date",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Filtered Dataset",
        data=csv,
        file_name="ecommerce_filtered_data.csv",
        mime="text/csv"
    )

    summary = category_analysis(filtered)

    st.download_button(
        "⬇️ Download Category Summary",
        data=summary.to_csv(index=False).encode("utf-8"),
        file_name="category_summary.csv",
        mime="text/csv"
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "E-Commerce Sales & Business Analytics | "
    "Portfolio Project | Dataset is synthetically "
    "generated for educational and analytical demonstration."
)
