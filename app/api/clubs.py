from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.club import Club

router = APIRouter()


@router.get("/clubs")
def list_clubs(db: Session = Depends(get_db)):
    return db.query(Club).all()