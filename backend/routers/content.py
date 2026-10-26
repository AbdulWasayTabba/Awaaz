from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from core.deps import get_current_user
from db.models import Phoneme, PracticeItem, User
from db.session import get_db
from schemas.content import Item_Out, Sound_Out

router = APIRouter(prefix="/content", tags=["content"])

LANG = "ur"
PUBLISHED = "published"

# show items in the order a therapist would teach them
POSITION_ORDER = case(
    {"initial": 0, "medial": 1, "final": 2},
    value=PracticeItem.position,
    else_=3,
)


@router.get("/sounds", response_model=list[Sound_Out])
def list_sounds(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Target sounds that have at least one published practice item."""
    rows = db.execute(
        select(Phoneme, func.count(PracticeItem.id))
        .join(PracticeItem, PracticeItem.target_phoneme_id == Phoneme.id)
        .where(PracticeItem.status == PUBLISHED, Phoneme.language_code == LANG)
        .group_by(Phoneme.id)
        .order_by(Phoneme.sort_order)
    ).all()
    return [
        Sound_Out(code=p.label, ipa=p.ipa, manner=p.manner, item_count=n)
        for p, n in rows
    ]


@router.get("/items", response_model=list[Item_Out])
def list_items(
    sound: Optional[str] = Query(None, description="CISAMPA code, e.g. K or TT"),
    position: Optional[Literal["initial", "medial", "final"]] = None,
    tier: Literal["sound", "word", "sentence"] = "word",
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Published practice items, optionally filtered by sound and position."""
    if sound is not None:
        known = db.scalar(
            select(Phoneme.id).where(
                Phoneme.language_code == LANG, Phoneme.label == sound
            )
        )
        if known is None:
            raise HTTPException(status_code=404, detail=f"Unknown sound '{sound}'")

    stmt = (
        select(PracticeItem, Phoneme)
        .join(Phoneme, Phoneme.id == PracticeItem.target_phoneme_id)
        .where(
            PracticeItem.status == PUBLISHED,
            PracticeItem.language_code == LANG,
            PracticeItem.tier == tier,
        )
        .order_by(Phoneme.sort_order, POSITION_ORDER, PracticeItem.transliteration)
    )
    if sound is not None:
        stmt = stmt.where(Phoneme.label == sound)
    if position is not None:
        stmt = stmt.where(PracticeItem.position == position)

    return [
        Item_Out(
            id=item.id,
            text=item.text_native,
            transliteration=item.transliteration,
            gloss=item.gloss_en,
            ipa=item.ipa,
            tier=item.tier,
            position=item.position,
            sound=ph.label,
            sound_ipa=ph.ipa,
        )
        for item, ph in db.execute(stmt).all()
    ]