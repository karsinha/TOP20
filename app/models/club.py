from sqlalchemy import Boolean, Column, Integer, String

from app.db.base import Base


class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=True)
    primary_color = Column(String, nullable=True)
    secondary_color = Column(String, nullable=True)
    division = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    description = Column(String, nullable=True)