import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

DATABASE_URL = "postgresql://postgresql_jztr_user:XKajGhxhz6OY25fXrROMzBAbGYHfp42s@dpg-d7tnfmosfn5c73enlgq0-a.oregon-postgres.render.com/postgresql_jztr"


@st.cache_data(ttl=60)
def load_data():
    conn = psycopg2.connect(DATABASE_URL)
    df = pd.read_sql("SELECT * FROM opportunities;", conn)
    conn.close()

    if "score" not in df.columns:
        df["score"] = "Website"

    if "source" not in df.columns:
        df["source"] = "MIS Opportunity Hub"

    if "company" not in df.columns:
        df["company"] = "Unknown"

    if "location" not in df.columns:
        df["location"] = "Unknown"

    return df


st.set_page_config(
    page_title="MIS Jobs Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 MIS Jobs Dashboard")
st.write("Dashboard connected directly to PostgreSQL database")

df = load_data()

st.metric("Total Jobs", len(df))

left1, right1 = st.columns(2)

with left1:
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

with right1:
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
    title="Top Companies by Number of Jobs"
)
st.plotly_chart(fig_company, use_container_width=True)

st.divider()

st.subheader("Jobs Table")
st.dataframe(df, use_container_width=True)