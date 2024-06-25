"""
  Now is easy to implement the database repository. The DBRepository
  should implement the Repository (Storage) interface and the methods defined
  in the abstract class Storage.

  The methods to implement are:
    - get_all
    - get
    - save
    - update
    - delete
    - reload (which can be empty)
"""

from src.models.base import Base
from src.persistence.repository import Repository


class DBRepository(Repository):
    def __init__(self) -> None: ...

    def get_all(self, model_name: str) -> list:
        return []

    def get(self, model_name: str, obj_id: str): ...

    def reload(self): ...

    def save(self, obj: Base): ...

    def update(self, obj: Base): ...

    def delete(self, obj: Base) -> bool:
        return False
