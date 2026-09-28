from sqlalchemy import Column, ForeignKey, Integer

from app.db.base import Base


class CategoryItem(Base):
    __tablename__ = "category_items"

    category_id = Column(Integer, ForeignKey("categories.id"), primary_key=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), primary_key=True)
    sort_key = Column(Integer, nullable=True)