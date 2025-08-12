from typing import LiteralString

from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String
from app.setup.database import Base


class User(Base):
    id: Mapped[int] = Column(Integer, primary_key=True)

    name: Mapped[str] = Column(String(100), nullable=False)
    email: Mapped[str | LiteralString] = Column(String(100), nullable=False, unique=True)
