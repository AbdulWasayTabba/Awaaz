"""Run once before the first migration:  python create_schemas.py"""
from sqlalchemy import text
from db.session import engine

SCHEMAS = ["app", "scoring", "billing", "audit", "linkage", "reporting"]

with engine.begin() as conn:
    for s in SCHEMAS:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {s}"))
print("schemas ready:", ", ".join(SCHEMAS))