from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.category import Category
from app.models.category_item import CategoryItem
from app.models.club import Club

CATEGORY_SLUG = "argentine-football"
CATEGORY_VERSION = 1

# slug, name, short_name, primary_color, secondary_color
CLUBS = [
    ("river-plate", "River Plate", "River", "#E4002B", "#FFFFFF"),
    ("boca-juniors", "Boca Juniors", "Boca", "#003A70", "#FFC800"),
    ("san-lorenzo", "San Lorenzo", "San Lorenzo", "#002D62", "#C8102E"),
    ("independiente", "Independiente", "Independiente", "#D81E05", "#FFFFFF"),
    ("racing-club", "Racing Club", "Racing", "#6CACE4", "#FFFFFF"),
    ("velez-sarsfield", "Vélez Sarsfield", "Vélez", "#003DA5", "#FFFFFF"),
    ("estudiantes-lp", "Estudiantes de La Plata", "Estudiantes", "#E4002B", "#FFFFFF"),
    ("gimnasia-lp", "Gimnasia y Esgrima La Plata", "Gimnasia", "#003DA5", "#FFFFFF"),
    ("huracan", "Huracán", "Huracán", "#FFFFFF", "#E4002B"),
    ("newells-old-boys", "Newell's Old Boys", "Newell's", "#C8102E", "#000000"),
    ("rosario-central", "Rosario Central", "Central", "#002F6C", "#FFD100"),
    ("lanus", "Lanús", "Lanús", "#7A1F3D", "#FFFFFF"),
    ("argentinos-juniors", "Argentinos Juniors", "Argentinos", "#D81E05", "#FFFFFF"),
    ("platense", "Platense", "Platense", "#5C3A21", "#FFFFFF"),
    ("banfield", "Banfield", "Banfield", "#1E8449", "#FFFFFF"),
    ("colon", "Colón de Santa Fe", "Colón", "#D81E05", "#000000"),
    ("ferro", "Ferro Carril Oeste", "Ferro", "#0B6E3A", "#FFFFFF"),
    ("union", "Unión de Santa Fe", "Unión", "#D81E05", "#FFFFFF"),
    ("talleres", "Talleres de Córdoba", "Talleres", "#1F3A93", "#FFFFFF"),
    ("belgrano", "Belgrano de Córdoba", "Belgrano", "#5DADE2", "#FFFFFF"),
    ("tigre", "Tigre", "Tigre", "#1F4E9C", "#C8102E"),
    ("arsenal", "Arsenal de Sarandí", "Arsenal", "#6CB4EE", "#C8102E"),
    ("quilmes", "Quilmes", "Quilmes", "#FFFFFF", "#0057B8"),
    ("chacarita-juniors", "Chacarita Juniors", "Chacarita", "#C8102E", "#000000"),
    ("godoy-cruz", "Godoy Cruz", "Godoy Cruz", "#003DA5", "#FFFFFF"),
]


def seed() -> None:
    with SessionLocal() as db:
        # 1) Clubs: create or update by slug
        clubs = []
        for slug, name, short_name, primary, secondary in CLUBS:
            club = db.scalar(select(Club).where(Club.slug == slug))
            if club is None:
                club = Club(slug=slug)
                db.add(club)
            club.name = name
            club.short_name = short_name
            club.primary_color = primary
            club.secondary_color = secondary
            clubs.append(club)
        db.flush()  # assigns ids to the new clubs

        # 2) Category: create if it doesn't exist
        category = db.scalar(
            select(Category).where(
                Category.slug == CATEGORY_SLUG,
                Category.version == CATEGORY_VERSION,
            )
        )
        if category is None:
            category = Category(slug=CATEGORY_SLUG, version=CATEGORY_VERSION)
            db.add(category)
        category.name = "Biggest Argentine football clubs"
        category.pool_size = len(CLUBS)
        category.ranking_size = 20
        db.flush()

        # 3) Candidate pool: link clubs to the category
        for index, club in enumerate(clubs):
            item = db.get(CategoryItem, (category.id, club.id))
            if item is None:
                db.add(CategoryItem(category_id=category.id, club_id=club.id, sort_key=index))
            else:
                item.sort_key = index

        db.commit()
        print(f"Seeded {len(clubs)} clubs and category '{CATEGORY_SLUG}' v{CATEGORY_VERSION}")


if __name__ == "__main__":
    seed()