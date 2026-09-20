# AI SQL Server Data Analyst

A safety-first Streamlit application that lets analysts ask business questions, generate SQL with a free local Ollama model, validate the query, execute it against Microsoft SQL Server, and download the result.

## Business value

- Reduces the time required to convert questions into SQL
- Keeps generated queries read-only by default
- Produces interactive tables and charts
- Exports query results to CSV
- Uses local AI through Ollama, avoiding paid API requirements

## Architecture

```text
Business question → Ollama → SQL validator → SQL Server → DataFrame → chart/export
```

## Features

- Microsoft SQL Server connection through SQLAlchemy and ODBC
- Schema-aware SQL generation
- Read-only query guard against destructive statements
- Row limits to reduce accidental large extracts
- Streamlit interface with automatic numeric charts
- Direct SQL mode for experienced analysts
- Unit tests for query validation

## Quick start

1. Install Python 3.11+, Microsoft ODBC Driver 18 and [Ollama](https://ollama.com/).
2. Download a model: `ollama pull llama3.1:8b`.
3. Install dependencies:

```bash
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

4. Add your SQL Server connection values to `.env`.

> Use a database account with SELECT-only permissions. Never commit your `.env` file.

## Testing

```bash
pytest
```

## Technology

Python · Streamlit · Microsoft SQL Server · SQLAlchemy · pandas · Plotly · Ollama · pytest

## Portfolio note

This is an original portfolio implementation designed around common analytics controls: least-privilege access, query validation, result limits and auditable SQL.
