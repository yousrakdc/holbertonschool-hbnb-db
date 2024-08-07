from src.persistence import Repository
from src.persistence.db import db


def populate_db(db: Repository) -> None:
    from src.models.country import Country

    countries = [
        Country(name="Uruguay", code="UY"),
    ]
    
    for country in countries:
        db.save(country)

    print("Memory DB populated")
