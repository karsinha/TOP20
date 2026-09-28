from sqlalchemy import Boolean, Column, Integer, String, UniqueConstraint

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("slug", "version", name="uq_category_slug_version"),)

    id = Column(Integer, primary_key=True)
    slug = Column(String, nullable=False, index=True)
    version = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    pool_size = Column(Integer, nullable=False)
    ranking_size = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)