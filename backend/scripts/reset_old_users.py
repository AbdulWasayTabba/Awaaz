"""One-time cleanup of the earlier test migration (public.users + alembic_version)."""
from sqlalchemy import text
from db.session import engine

with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS public.users CASCADE"))
    conn.execute(text("DROP TYPE IF EXISTS userrole CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS public.alembic_version"))
print("old test tables removed")