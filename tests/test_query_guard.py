from src.query_guard import clean_sql, enforce_top, validate_read_only

def test_select_allowed():
    assert validate_read_only("SELECT * FROM orders")[0]

def test_cte_allowed():
    assert validate_read_only("WITH x AS (SELECT 1 AS n) SELECT * FROM x")[0]

def test_destructive_query_blocked():
    ok, _ = validate_read_only("DELETE FROM orders")
    assert not ok

def test_multiple_statements_blocked():
    assert not validate_read_only("SELECT 1; SELECT 2")[0]

def test_top_is_added():
    assert enforce_top("SELECT * FROM orders").startswith("SELECT TOP 500")

def test_fence_removed():
    assert clean_sql("```sql\nSELECT 1;\n```") == "SELECT 1"
