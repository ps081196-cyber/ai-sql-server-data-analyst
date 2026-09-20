"""Validation utilities for model-generated SQL."""
import re

FORBIDDEN = {
    "insert", "update", "delete", "drop", "alter", "truncate", "merge",
    "create", "grant", "revoke", "execute", "exec", "backup", "restore",
}

def clean_sql(sql: str) -> str:
    sql = re.sub(r"^```(?:sql)?|\```$", "", sql.strip(), flags=re.I).strip()
    return sql.rstrip(";").strip()

def validate_read_only(sql: str) -> tuple[bool, str]:
    candidate = clean_sql(sql)
    if not candidate:
        return False, "Query is empty."
    lowered = re.sub(r"--.*?$|/\*.*?\*/", " ", candidate.lower(), flags=re.M | re.S)
    tokens = set(re.findall(r"[a-z_]+", lowered))
    blocked = sorted(tokens & FORBIDDEN)
    if blocked:
        return False, f"Blocked statement: {', '.join(blocked)}"
    if not re.match(r"^(select|with)\b", lowered.strip()):
        return False, "Only SELECT or CTE queries are allowed."
    if ";" in candidate:
        return False, "Multiple SQL statements are not allowed."
    return True, "Read-only query accepted."

def enforce_top(sql: str, limit: int = 500) -> str:
    candidate = clean_sql(sql)
    if re.match(r"^select\s+(?!top\s)", candidate, flags=re.I):
        return re.sub(r"^select\s+", f"SELECT TOP {limit} ", candidate, count=1, flags=re.I)
    return candidate
