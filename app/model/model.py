from typing import LiteralString

from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.setup.database import Base


class User(Base):
    id: Mapped[int] = Column(Integer, primary_key=True)

    name: Mapped[str] = Column(String(100), nullable=False)
    email: Mapped[str | LiteralString] = Column(String(100), nullable=False, unique=True)

    otps = relationship("Otp", back_populates="user", cascade="all, delete-orphan")


class Otp(Base):
    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    code: Mapped[str] = Column(String(12), nullable=False)
    expires_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)
    last_sent_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="otps")
