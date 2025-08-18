from __future__ import annotations

import uuid
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.model.model import Passage, PracticeQuestion


class PracticeCrud:
    @classmethod
    async def get_listening_passages_with_questions(cls, db: AsyncSession, limit: int = 10) -> List[Passage]:
        """
        Get listening passages with their associated questions.
        Returns passages ordered by creation date (newest first).
        """
        # Get passages for listening skill
        result = await db.execute(
            select(Passage).where(Passage.skill == "listening").order_by(Passage.created_at.desc()).limit(limit)
        )
        passages = result.scalars().all()

        # For each passage, fetch its questions
        for passage in passages:
            questions_result = await db.execute(
                select(PracticeQuestion)
                .where(PracticeQuestion.passage_id == passage.id)
                .order_by(PracticeQuestion.created_at.asc())
            )
            passage.questions = questions_result.scalars().all()

        return passages

    @classmethod
    async def get_reading_passages_with_questions(cls, db: AsyncSession, limit: int = 10) -> List[Passage]:
        """
        Get reading passages with their associated questions.
        Returns passages ordered by creation date (newest first).
        """
        # Get passages for reading skill
        result = await db.execute(
            select(Passage).where(Passage.skill == "reading").order_by(Passage.created_at.desc()).limit(limit)
        )
        passages = result.scalars().all()

        # For each passage, fetch its questions
        for passage in passages:
            questions_result = await db.execute(
                select(PracticeQuestion)
                .where(PracticeQuestion.passage_id == passage.id)
                .order_by(PracticeQuestion.created_at.asc())
            )
            passage.questions = questions_result.scalars().all()

        return passages

    @classmethod
    async def get_speaking_questions(cls, db: AsyncSession, limit: int = 10) -> List[PracticeQuestion]:
        """
        Get speaking practice questions.
        Returns questions ordered by creation date (newest first).
        """
        # Get questions for speaking skill (no passage_id since speaking questions are standalone)
        result = await db.execute(
            select(PracticeQuestion)
            .where(PracticeQuestion.skill == "speaking")
            .where(PracticeQuestion.passage_id.is_(None))  # Speaking questions don't have passages
            .order_by(PracticeQuestion.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

    @classmethod
    async def get_passage_by_id(cls, db: AsyncSession, passage_id: uuid.UUID) -> Optional[Passage]:
        """Get a single passage by ID"""
        result = await db.execute(select(Passage).where(Passage.id == passage_id).limit(1))
        return result.scalar_one_or_none()

    @classmethod
    async def get_questions_by_passage_id(cls, db: AsyncSession, passage_id: uuid.UUID) -> List[PracticeQuestion]:
        """Get all questions for a specific passage"""
        result = await db.execute(
            select(PracticeQuestion)
            .where(PracticeQuestion.passage_id == passage_id)
            .order_by(PracticeQuestion.created_at.asc())
        )
        return result.scalars().all()

    @classmethod
    async def get_writing_prompts(cls, db: AsyncSession, limit: int = 10) -> List[PracticeQuestion]:
        """
        Get writing practice prompts.
        Returns prompts ordered by creation date (newest first).
        """
        # Get questions for writing skill (no passage_id since writing prompts are standalone)
        result = await db.execute(
            select(PracticeQuestion)
            .where(PracticeQuestion.skill == "writing")
            .where(PracticeQuestion.passage_id.is_(None))  # Writing prompts don't have passages
            .order_by(PracticeQuestion.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
