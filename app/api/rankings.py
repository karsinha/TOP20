from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.ranking import RankingCreate, RankingRead
from app.services.ranking_rules import InvalidRankingError
from app.services.ranking_service import (
    UnknownFanClubError,
    get_active_category,
    submit_ranking,
)

router = APIRouter(prefix="/rankings", tags=["rankings"])


@router.post("", response_model=RankingRead, status_code=201)
def create_ranking(
    payload: RankingCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    category = get_active_category(db, payload.category_slug)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    try:
        ranking = submit_ranking(
            db, user, category, payload.club_ids, payload.fan_club_id
        )
    except (InvalidRankingError, UnknownFanClubError) as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    return RankingRead(
        id=ranking.id,
        category_id=ranking.category_id,
        fan_club_id=ranking.fan_club_id,
        club_ids=payload.club_ids,
        updated_at=ranking.updated_at,
    )