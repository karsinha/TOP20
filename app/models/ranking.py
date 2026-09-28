from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)

from app.db.base import Base


class Ranking(Base):
    __tablename__ = "rankings"
    __table_args__ = (UniqueConstraint("user_id", "category_id", name="uq_ranking_user_category"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    fan_club_id = Column(Integer, ForeignKey("clubs.id"), nullable=True)
    excluded = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)