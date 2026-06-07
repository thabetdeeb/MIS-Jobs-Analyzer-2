import streamlit as st
import pandas as pd
import plotly.express as px


EXCEL_FILE = "north_is_jobs_analysis.xlsx"

st.set_page_config(
    page_title="MIS Jobs Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 MIS Jobs Dashboard")
st.write("Dashboard for Information Systems jobs in Northern Israel")

try:
    df = pd.read_excel(EXCEL_FILE)
except FileNotFoundError:
    st.error("Excel file was not found. Please run main.py first.")
    st.stop()

if df.empty:
    st.warning("Excel file is empty. No jobs found.")
    st.stop()

if "source" not in df.columns:
    df["source"] = "Unknown"

total_jobs = len(df)
total_companies = df["company"].nunique()
top_location = df["location"].value_counts().idxmax()
top_category = df["category"].value_counts().idxmax()
top_source = df["source"].value_counts().idxmax()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Jobs", total_jobs)
col2.metric("Companies", total_companies)
col3.metric("Top Location", top_location)
col4.metric("Top Category", top_category)
col5.metric("Top Source", top_source)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Jobs by Location")
    location_counts = df["location"].value_counts().reset_index()
    location_counts.columns = ["location", "count"]

    fig_location = px.bar(
        location_counts,
        x="location",
        y="count",
        text="count",
        title="Number of Jobs by Location"
    )
    st.plotly_chart(fig_location, use_container_width=True)

with right:
    st.subheader("Jobs by Category")
    category_counts = df["category"].value_counts().reset_index()
    category_counts.columns = ["category", "count"]

    fig_category = px.pie(
        category_counts,
        names="category",
        values="count",
        title="Jobs Percentage by Category",
        hole=0.4
    )
    st.plotly_chart(fig_category, use_container_width=True)

st.divider()

left2, right2 = st.columns(2)

with left2:
    st.subheader("Jobs by Source")
    source_counts = df["source"].value_counts().reset_index()
    source_counts.columns = ["source", "count"]

    fig_source = px.bar(
        source_counts,
        x="source",
        y="count",
        text="count",
        title="Number of Jobs by Source"
    )
    st.plotly_chart(fig_source, use_container_width=True)

with right2:
    st.subheader("Jobs by Score")
    score_counts = df["score"].value_counts().sort_index().reset_index()
    score_counts.columns = ["score", "count"]

    fig_score = px.bar(
        score_counts,
        x="score",
        y="count",
        text="count",
        title="Jobs by Matching Score"
    )
    st.plotly_chart(fig_score, use_container_width=True)

st.divider()

st.subheader("Top Companies")
company_counts = df["company"].value_counts().head(10).reset_index()
company_counts.columns = ["company", "count"]

fig_company = px.bar(
    company_counts,
    x="company",
    y="count",
    text="count",
    title="Top 10 Companies by Number of Jobs"
)
st.plotly_chart(fig_company, use_container_width=True)

st.divider()

st.subheader("Jobs Table")

search_text = st.text_input("Search by title, company, location, category or source")

filtered_df = df.copy()

if search_text:
    search_text = search_text.lower()
    filtered_df = filtered_df[
        filtered_df.astype(str).apply(
            lambda row: row.str.lower().str.contains(search_text).any(),
            axis=1
        )
    ]

st.dataframe(filtered_df, use_container_width=True)