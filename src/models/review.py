from src.models.base import Base
from src.models.place import Place
from src.models.user import User
from src import db
from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime, Boolean, Text, Float
from datetime import datetime


class Review(Base):

    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    comment = Column(Text, nullable=False)
    rating = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(
        self, place_id: str, user_id: str, comment: str, rating: float, **kw
    ) -> None:
        super().__init__(**kw)

        self.place_id = place_id
        self.user_id = user_id
        self.comment = comment
        self.rating = rating

    def __repr__(self) -> str:
        return f"<Review {self.id} - '{self.comment[:25]}...'>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Review":
        from src.persistence import db

        user: User | None = User.get(data["user_id"])

        if not user:
            raise ValueError(f"User with ID {data['user_id']} not found")

        place: Place | None = Place.get(data["place_id"])

        if not place:
            raise ValueError(f"Place with ID {data['place_id']} not found")

        new_review = Review(**data)

        db.save(new_review)

        return new_review

    @staticmethod
    def update(review_id: str, data: dict) -> "Review | None":
        from src.persistence import db

        review = Review.get(review_id)

        if not review:
            raise ValueError("Review not found")

        for key, value in data.items():
            setattr(review, key, value)

        db.update(review)

        return review