from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.category_item import CategoryItem
from app.models.club import Club
from app.models.ranking import Ranking
from app.models.ranking_position import RankingPosition
from app.models.user import User
from app.services.ranking_rules import validate_ranking


class UnknownFanClubError(ValueError):
    """Raised when fan_club_id does not match any club."""


def get_active_category(db: Session, slug: str) -> Category | None:
    return db.scalar(
        select(Category)
        .where(Category.slug == slug, Category.is_active.is_(True))
        .order_by(Category.version.desc())
        .limit(1)
    )


def submit_ranking(
    db: Session,
    user: User,
    category: Category,
    club_ids: list[int],
    fan_club_id: int | None,
) -> Ranking:
    pool_ids = set(
        db.scalars(
            select(CategoryItem.club_id).where(CategoryItem.category_id == category.id)
        ).all()
    )
    validate_ranking(club_ids, pool_ids, category.ranking_size)

    if fan_club_id is not None and db.get(Club, fan_club_id) is None:
        raise UnknownFanClubError(f"Unknown fan club: {fan_club_id}")

    ranking = db.scalar(
        select(Ranking).where(
            Ranking.user_id == user.id, Ranking.category_id == category.id
        )
    )
    if ranking is None:
        ranking = Ranking(
            user_id=user.id, category_id=category.id, fan_club_id=fan_club_id
        )
        db.add(ranking)
    else:
        ranking.fan_club_id = fan_club_id
        ranking.updated_at = func.now()
        db.execute(
            delete(RankingPosition).where(RankingPosition.ranking_id == ranking.id)
        )
    db.flush()

    db.add_all(
        RankingPosition(ranking_id=ranking.id, club_id=club_id, position=position)
        for position, club_id in enumerate(club_ids, start=1)
    )
    db.commit()
    db.refresh(ranking)
    return ranking