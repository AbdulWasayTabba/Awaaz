from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.deps import require_therapist
from db.models import CareAssignment, Child, User
from db.session import get_db
from routers.children import to_child_out
from schemas.children import Child_Out

router = APIRouter(prefix="/therapist", tags=["therapist"])


@router.get("/caseload", response_model=list[Child_Out])
def caseload(user: User = Depends(require_therapist), db: Session = Depends(get_db)):

    children = db.scalars(select(Child).join(CareAssignment, CareAssignment.child_id == Child.id)
                                       .where(
                                           CareAssignment.therapist_user_id == user.id,
                                           CareAssignment.ended_at.is_(None),
                                       )
                                       .distinct()
                                       .order_by(Child.created_at)
                                       ).all()
    return [to_child_out(c, is_linked = True) for c in children]

 