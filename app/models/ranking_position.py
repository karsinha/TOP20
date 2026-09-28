from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, SmallInteger, UniqueConstraint

from app.db.base import Base


class RankingPosition(Base):
    __tablename__ = "ranking_positions"
    __table_args__ = (
        CheckConstraint("position >= 1", name="ck_position_positive"),
        UniqueConstraint("ranking_id", "position", name="uq_ranking_position"),
    )

    ranking_id = Column(Integer, ForeignKey("rankings.id"), primary_key=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), primary_key=True)
    position = Column(SmallInteger, nullable=False)