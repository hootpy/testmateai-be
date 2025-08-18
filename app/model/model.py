import uuid
from datetime import datetime
from typing import LiteralString, Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql.schema import Column

from app.setup.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name: Mapped[str] = Column(String(255), nullable=False)
    email: Mapped[str | LiteralString] = Column(String(255), nullable=False, unique=True)
    current_score: Mapped[Optional[float]] = Column(Numeric(3, 1), nullable=True, server_default=text("0"))
    target_score: Mapped[Optional[float]] = Column(Numeric(3, 1), nullable=True, server_default=text("7.0"))
    test_date: Mapped[Optional[Date]] = Column(Date, nullable=True)
    has_previous_test: Mapped[bool] = Column(Boolean, nullable=False, server_default=text("FALSE"))
    last_test_score: Mapped[Optional[float]] = Column(Numeric(3, 1), nullable=True)
    level: Mapped[int] = Column(Integer, nullable=False, server_default=text("1"))
    xp: Mapped[int] = Column(Integer, nullable=False, server_default=text("0"))
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )


class OtpCode(Base):
    __tablename__ = "otp_codes"

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    email: Mapped[str] = Column(String(255), nullable=False)
    otp_code: Mapped[str] = Column(String(6), nullable=False)
    expires_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)
    used: Mapped[bool] = Column(Boolean, nullable=False, server_default=text("FALSE"))
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )


class Passage(Base):
    __tablename__ = "passages"

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    title: Mapped[str] = Column(String(255), nullable=False)
    content: Mapped[str] = Column(Text, nullable=False)
    skill: Mapped[str] = Column(String(50), nullable=False)
    question_type: Mapped[str] = Column(String(50), nullable=False)
    difficulty_level: Mapped[str] = Column(String(20), nullable=False, server_default=text("'intermediate'"))
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )


class PracticeQuestion(Base):
    __tablename__ = "practice_questions"

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    skill: Mapped[str] = Column(String(50), nullable=False)
    question_type: Mapped[str] = Column(String(50), nullable=False)
    passage_id: Mapped[Optional[uuid.UUID]] = Column(UUID(as_uuid=True), ForeignKey("passages.id"), nullable=True)
    question_text: Mapped[str] = Column(Text, nullable=False)
    options: Mapped[Optional[dict]] = Column(JSONB, nullable=True)
    correct_answer: Mapped[Optional[str]] = Column(Text, nullable=True)
    explanation: Mapped[Optional[str]] = Column(Text, nullable=True)
    difficulty_level: Mapped[str] = Column(String(20), nullable=False, server_default=text("'intermediate'"))
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )


class MockTest(Base):
    __tablename__ = "mock_tests"

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[Optional[str]] = Column(Text, nullable=True)
    duration: Mapped[int] = Column(Integer, nullable=False)
    sections: Mapped[dict] = Column(JSONB, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )


class UserActivity(Base):
    __tablename__ = "user_activities"

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    type: Mapped[str] = Column(String(50), nullable=False)
    practice_type: Mapped[Optional[str]] = Column(String(50), nullable=True)
    score: Mapped[Optional[float]] = Column(Numeric(3, 1), nullable=True)
    band: Mapped[Optional[float]] = Column(Numeric(3, 1), nullable=True)
    details: Mapped[Optional[dict]] = Column(JSONB, nullable=True)
    xp_earned: Mapped[int] = Column(Integer, nullable=False, server_default=text("0"))
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )


class Vocabulary(Base):
    __tablename__ = "vocabulary"

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    word: Mapped[str] = Column(String(255), nullable=False)
    definition: Mapped[Optional[str]] = Column(Text, nullable=True)
    source: Mapped[str] = Column(String(50), nullable=False, server_default=text("'practice'"))
    reviewed: Mapped[bool] = Column(Boolean, nullable=False, server_default=text("FALSE"))
    mastered: Mapped[bool] = Column(Boolean, nullable=False, server_default=text("FALSE"))
    notes: Mapped[Optional[str]] = Column(Text, nullable=True)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    template_id: Mapped[Optional[uuid.UUID]] = Column(UUID(as_uuid=True), nullable=True)
    customizations: Mapped[Optional[dict]] = Column(JSONB, nullable=True)
    current_week: Mapped[int] = Column(Integer, nullable=False, server_default=text("1"))
    progress: Mapped[Optional[dict]] = Column(JSONB, nullable=True)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )


class AiFeedback(Base):
    __tablename__ = "ai_feedback"

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    activity_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey("user_activities.id"), nullable=False, index=True
    )
    skill: Mapped[str] = Column(String(50), nullable=False)
    feedback_data: Mapped[dict] = Column(JSONB, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
