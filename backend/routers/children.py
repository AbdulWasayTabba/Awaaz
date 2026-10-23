from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.deps import get_current_user
from db.models import Child, Guardianship, User
from db.session import get_db
from schemas.children import Child_Create, Child_Out

router = APIRouter(prefix="/children", tags=["children"])


def age_in_months(dob: date) -> int:
    today = date.today()
    months = (today.year - dob.year) * 12 + (today.month - dob.month)
    if today.day < dob.day:  # hasn't reached this month's "birthday" yet
        months -= 1
    return months


def to_child_out(child: Child) -> Child_Out:
    # translate database names (nickname, date_of_birth) to API names (name, dob)
    return Child_Out(
        id=child.id,
        name=child.nickname,
        dob=child.date_of_birth,
        age_in_months=age_in_months(child.date_of_birth),
    )


@router.post("", response_model=Child_Out, status_code=201)
def create_child(body: Child_Create,user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    child = Child(
        nickname=body.name,
        date_of_birth=body.dob,
        sex=body.sex,
        timezone="Asia/Karachi",
        status="active",
        created_via="parent",
        created_by_user_id=user.id,
    )
    db.add(child)
    db.flush()  # sends the INSERT so child.id exists; nothing is committed yet

    db.add(Guardianship(
        child_id=child.id,
        user_id=user.id,
        relationship="parent",
        source="parent",
        started_at=datetime.now(timezone.utc),
    ))

    db.commit()  # child and guardianship are saved together, or not at all
    db.refresh(child)
    return to_child_out(child)


@router.get("", response_model=list[Child_Out])
def list_my_children(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # only children this user actively guards (guardianship not ended)
    children = db.scalars(
        select(Child)
        .join(Guardianship, Guardianship.child_id == Child.id)
        .where(Guardianship.user_id == user.id, Guardianship.ended_at.is_(None))
        .order_by(Child.created_at)
    ).all()
    return [to_child_out(c) for c in children]