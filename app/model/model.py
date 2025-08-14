from typing import LiteralString, Optional

from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql.schema import Column
from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Float,
    Date,
    Text,
    JSON,
)
from datetime import datetime
from app.setup.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True)
    email: Mapped[str | LiteralString] = Column(String(255), nullable=False, unique=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    level: Mapped[int] = Column(Integer, nullable=False, default=0)
    xp: Mapped[int] = Column(Integer, nullable=False, default=0)
    target_score: Mapped[Optional[float]] = Column(Float, nullable=True)
    test_date: Mapped[Optional[Date]] = Column(Date, nullable=True)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)


class OtpCode(Base):
    __tablename__ = "otp_codes"

    id: Mapped[int] = Column(Integer, primary_key=True)
    email: Mapped[str] = Column(String(255), nullable=False, index=True)
    otp: Mapped[str] = Column(String(12), nullable=False)
    expires_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)


class TestSession(Base):
    __tablename__ = "test_sessions"

    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    test_type: Mapped[str] = Column(String(50), nullable=False)
    difficulty: Mapped[str] = Column(String(50), nullable=True)
    score: Mapped[Optional[float]] = Column(Float, nullable=True)
    band: Mapped[Optional[float]] = Column(Float, nullable=True)
    time_spent: Mapped[Optional[int]] = Column(Integer, nullable=True)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)


class TestAnswer(Base):
    __tablename__ = "test_answers"

    id: Mapped[int] = Column(Integer, primary_key=True)
    session_id: Mapped[int] = Column(
        Integer, ForeignKey("test_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_id: Mapped[int] = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_answer: Mapped[Optional[str]] = Column(Text, nullable=True)
    is_correct: Mapped[Optional[bool]] = Column(Boolean, nullable=True)
    feedback: Mapped[Optional[str]] = Column(Text, nullable=True)


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = Column(Text, nullable=True)
    icon: Mapped[Optional[str]] = Column(String(255), nullable=True)
    criteria: Mapped[Optional[dict]] = Column(JSON, nullable=True)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    achievement_id: Mapped[int] = Column(Integer, ForeignKey("achievements.id", ondelete="CASCADE"), primary_key=True)
    earned_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = Column(Integer, primary_key=True)
    test_type: Mapped[str] = Column(String(50), nullable=False)
    text: Mapped[str] = Column(Text, nullable=False)
    type: Mapped[str] = Column(String(50), nullable=False)
    options: Mapped[Optional[dict]] = Column(JSON, nullable=True)
    correct: Mapped[Optional[dict]] = Column(JSON, nullable=True)
    difficulty: Mapped[Optional[str]] = Column(String(50), nullable=True)
    topic: Mapped[Optional[str]] = Column(String(100), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    current_score: Mapped[Optional[float]] = Column(Float, nullable=True)
    target_score: Mapped[Optional[float]] = Column(Float, nullable=True)
    test_date: Mapped[Optional[Date]] = Column(Date, nullable=True)
    plan_data: Mapped[Optional[dict]] = Column(JSON, nullable=True)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)


class UserActivity(Base):
    __tablename__ = "user_activity"

    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    action: Mapped[str] = Column(String(100), nullable=False)
    details: Mapped[Optional[dict]] = Column(JSON, nullable=True)
    timestamp: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)


class TestAnalytics(Base):
    __tablename__ = "test_analytics"

    id: Mapped[int] = Column(Integer, primary_key=True)
    test_type: Mapped[str] = Column(String(50), nullable=False)
    average_score: Mapped[Optional[float]] = Column(Float, nullable=True)
    completion_rate: Mapped[Optional[float]] = Column(Float, nullable=True)
    date: Mapped[Date] = Column(Date, nullable=False)


class ContentUsage(Base):
    __tablename__ = "content_usage"

    id: Mapped[int] = Column(Integer, primary_key=True)
    content_id: Mapped[str] = Column(String(100), nullable=False)
    content_type: Mapped[str] = Column(String(50), nullable=False)
    usage_count: Mapped[int] = Column(Integer, nullable=False, default=0)
    date: Mapped[Date] = Column(Date, nullable=False)
