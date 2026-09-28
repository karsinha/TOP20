from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.club import Club
from app.schemas.club import ClubRead

router = APIRouter()


@router.get("/clubs", response_model=list[ClubRead])
def list_clubs(db: Session = Depends(get_db)):
    return db.scalars(select(Club).order_by(Club.name)).all()


@router.get("/clubs/{slug}", response_model=ClubRead)
def get_club(slug: str, db: Session = Depends(get_db)):
    club = db.scalar(select(Club).where(Club.slug == slug))
    if club is None:
        raise HTTPException(status_code=404, detail="Club not found")
    return club