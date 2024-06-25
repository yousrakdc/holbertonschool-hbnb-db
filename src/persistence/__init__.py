import os

from src.persistence.repository import Repository
from utils.constants import REPOSITORY_ENV_VAR

db: Repository

if os.getenv(REPOSITORY_ENV_VAR) == "db":
    from src.persistence.db import DBRepository

    db = DBRepository()
elif os.getenv(REPOSITORY_ENV_VAR) == "file":
    from src.persistence.file import FileRepository

    print("Using file repository")

    db = FileRepository()
else:
    from src.persistence.memory import MemoryRepository

    db = MemoryRepository()
