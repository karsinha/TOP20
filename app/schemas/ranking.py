from datetime import datetime

from pydantic import BaseModel


class RankingCreate(BaseModel):
    category_slug: str
    club_ids: list[int]          # ordered: index 0 = position 1
    fan_club_id: int | None = None


class RankingRead(BaseModel):
    id: int
    category_id: int
    fan_club_id: int | None
    club_ids: list[int]
    updated_at: datetime