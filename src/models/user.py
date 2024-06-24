from src.models.base import Base
from flask_sqlalchemy import SQLAlchemy
from src import db
from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime, Boolean
from datetime import datetime

class User(Base):

    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())

    def __init__(self, email: str, first_name: str, last_name: str, **kw) -> None:
        super().__init__(**kw)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self) -> str:
        return f"<User {self.id} ({self.email})>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(user: dict) -> "User":
        from src.persistence import db

        users: list["User"] = User.get_all()

        for u in users:
            if u.email == user["email"]:
                raise ValueError("User already exists")

        new_user = User(**user)

        db.save(new_user)

        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        from src.persistence import db

        user: User | None = User.get(user_id)

        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        db.update(user)

        return user