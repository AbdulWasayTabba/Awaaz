"""DEV ONLY: wipes every Awaaz schema and Alembic's version table."""
from sqlalchemy import text
from db.session import engine

SCHEMAS = ["app", "scoring", "billing", "audit", "linkage", "reporting"]

with engine.begin() as conn:
    for s in SCHEMAS:
        conn.execute(text(f"DROP SCHEMA IF EXISTS {s} CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS public.alembic_version"))
    conn.execute(text("DROP TABLE IF EXISTS public.users CASCADE"))
    conn.execute(text("DROP TYPE IF EXISTS userrole CASCADE"))
print("everything wiped")