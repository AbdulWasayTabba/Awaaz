import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.deps import get_current_user, require_therapist
from core.invites import generate_code, hash_code
from db.models import (CareAssignment, Enrollment, EnrollmentInvite, Guardianship,
                       OrgMembership, Organisation, User)
from db.session import get_db
from schemas.invites import EnrollmentOut, EnrollRequest, InviteOut

router = APIRouter(tags=["linking"])

INVITE_DAYS = 7


@router.post("/invites", response_model=InviteOut, status_code=201)
def create_invite(user: User = Depends(require_therapist), db: Session = Depends(get_db)):
    membership = db.scalar(select(OrgMembership).where(
        OrgMembership.user_id == user.id,
        OrgMembership.role == "therapist",
        OrgMembership.status == "active",
    ))
    if not membership:
        raise HTTPException(403, "No active therapist membership")

    code = generate_code()
    invite = EnrollmentInvite(
        org_id=membership.org_id,
        created_by_membership_id=membership.id,
        intended_discipline_key=membership.discipline_key,
        code_hash=hash_code(code),
        expires_at=datetime.now(timezone.utc) + timedelta(days=INVITE_DAYS),
    )
    db.add(invite)
    db.commit()
    return InviteOut(code=code, expires_at=invite.expires_at)  # the only time the code is shown


@router.post("/children/{child_id}/enroll", response_model=EnrollmentOut, status_code=201)
def enroll_child(
    child_id: uuid.UUID,
    body: EnrollRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # 1. the caller must be an active guardian of this child
    guardian = db.scalar(select(Guardianship).where(
        Guardianship.child_id == child_id,
        Guardianship.user_id == user.id,
        Guardianship.ended_at.is_(None),
    ))
    if not guardian:
        raise HTTPException(404, "Child not found")

    # 2. the code must exist and still be usable
    now = datetime.now(timezone.utc)
    invite = db.scalar(select(EnrollmentInvite).where(
        EnrollmentInvite.code_hash == hash_code(body.code)))
    if not invite or invite.revoked_at or invite.redeemed_at or invite.expires_at < now:
        raise HTTPException(400, "Invalid or expired code")

    # 3. the child must not already be enrolled in this practice
    already = db.scalar(select(Enrollment).where(
        Enrollment.child_id == child_id,
        Enrollment.org_id == invite.org_id,
        Enrollment.ended_at.is_(None),
    ))
    if already:
        raise HTTPException(409, "Child is already enrolled with this practice")

    # 4. the therapist who made the invite must still be active
    membership = db.get(OrgMembership, invite.created_by_membership_id)
    if not membership or membership.status != "active":
        raise HTTPException(400, "This therapist is no longer active")

    # 5. create both rows, then mark the invite as used: one transaction
    enrollment = Enrollment(
        child_id=child_id, org_id=invite.org_id, status="active",
        consent_method="in_app", consent_recorded_by=user.id, consent_recorded_at=now,
        enrollment_invite_id=invite.id, started_at=now, created_by_user_id=user.id,
    )
    db.add(enrollment)
    db.flush()  # gives enrollment.id

    db.add(CareAssignment(
        enrollment_id=enrollment.id, org_id=invite.org_id, child_id=child_id,
        org_membership_id=membership.id, membership_role=membership.role,
        discipline_key=membership.discipline_key, therapist_user_id=membership.user_id,
        started_at=now, created_by_user_id=user.id,
    ))
    invite.redeemed_by_user_id = user.id
    invite.redeemed_child_id = child_id
    invite.redeemed_at = now
    db.commit()

    org = db.get(Organisation, invite.org_id)
    therapist = db.get(User, membership.user_id)
    return EnrollmentOut(child_id=child_id, organisation=org.name, therapist=therapist.display_name)