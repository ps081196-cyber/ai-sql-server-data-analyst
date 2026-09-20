"""Streamlit interface for the AI SQL Server Data Analyst."""
import os
import requests
import streamlit as st
from dotenv import load_dotenv
import plotly.express as px

from src.database import build_engine, run_query, schema_summary
from src.query_guard import enforce_top, validate_read_only

load_dotenv()
st.set_page_config(page_title="AI SQL Server Analyst", page_icon="📊", layout="wide")
st.title("📊 AI SQL Server Data Analyst")
st.caption("Natural-language analysis with local Ollama and read-only SQL controls.")

@st.cache_resource
def engine():
    return build_engine()

def generate_sql(question: str, schema: str) -> str:
    prompt = f"""You are a Microsoft SQL Server analyst.
Return only one read-only SELECT query. Never modify data.
Limit results when appropriate. Schema:
{schema}
Question: {question}
"""
    response = requests.post(
        f"{os.getenv('OLLAMA_URL', 'http://localhost:11434')}/api/generate",
        json={"model": os.getenv("OLLAMA_MODEL", "llama3.1:8b"), "prompt": prompt, "stream": False},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["response"]

mode = st.radio("Input mode", ["Ask in natural language", "Write SQL"], horizontal=True)
user_input = st.text_area("Business question" if mode.startswith("Ask") else "SQL query", height=110)

if st.button("Run analysis", type="primary", disabled=not user_input.strip()):
    try:
        db = engine()
        sql = generate_sql(user_input, schema_summary(db)) if mode.startswith("Ask") else user_input
        sql = enforce_top(sql)
        valid, reason = validate_read_only(sql)
        st.code(sql, language="sql")
        if not valid:
            st.error(reason)
            st.stop()
        df = run_query(db, sql)
        st.success(f"Returned {len(df):,} rows.")
        st.dataframe(df, use_container_width=True)
        numeric = list(df.select_dtypes("number").columns)
        if numeric and len(df):
            category = next((c for c in df.columns if c not in numeric), None)
            if category:
                st.plotly_chart(px.bar(df.head(30), x=category, y=numeric[0]), use_container_width=True)
        st.download_button("Download CSV", df.to_csv(index=False), "analysis.csv", "text/csv")
    except Exception as exc:
        st.error(f"Analysis failed: {exc}")
