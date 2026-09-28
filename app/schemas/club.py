from pydantic import BaseModel, ConfigDict


class ClubRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str
    short_name: str | None
    primary_color: str | None
    secondary_color: str | None
    division: str | None
    is_active: bool
    description: str | None