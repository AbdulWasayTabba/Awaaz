"""Inserts reference data. Safe to run more than once."""
from db.session import SessionLocal
from db.models import AgeBand, Discipline, Language

LANGUAGES = [
    dict(code="en", name_en="English", name_native="English",
         is_ui_language=True, is_content_language=False),
    dict(code="ur", name_en="Urdu", name_native="اردو",
         is_ui_language=False, is_content_language=True),
]

DISCIPLINES = [
    dict(key="slt", name_en="Speech and language therapy", is_active=True),
]

# From the schema document: 3-4 = 36-59, 5-6 = 60-83, 7-8 = 84-119 months
AGE_BANDS = [
    dict(id=1, key="3-4", min_months=36, max_months=59),
    dict(id=2, key="5-6", min_months=60, max_months=83),
    dict(id=3, key="7-8", min_months=84, max_months=119),
]

with SessionLocal() as db:
    for model, rows in ((Language, LANGUAGES), (Discipline, DISCIPLINES), (AgeBand, AGE_BANDS)):
        for row in rows:
            db.merge(model(**row))
    db.commit()
    print("languages:", db.query(Language).count())
    print("disciplines:", db.query(Discipline).count())
    print("age bands:", db.query(AgeBand).count())