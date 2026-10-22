from sqlalchemy import text
from database import engine

query = """
select table_schema, count(*)
from information_schema.tables
where table_schema in ('app','scoring','billing','audit','linkage')
  and table_type = 'BASE TABLE'
group by 1
order by 1
"""

with engine.connect() as conn:
    for schema, n in conn.execute(text(query)):
        print(f"{schema:10} {n}")