from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User

DEV_GOOGLE_SUB = "dev-user"


def get_current_user(db: Session = Depends(get_db)) -> User:
    """TEMPORARY: replaced by real Google session auth in Phase 4."""
    user = db.scalar(select(User).where(User.google_sub == DEV_GOOGLE_SUB))
    if user is None:
        user = User(google_sub=DEV_GOOGLE_SUB)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user