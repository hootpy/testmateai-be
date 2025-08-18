from __future__ import annotations

import uuid
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.model.model import Vocabulary


class VocabularyCrud:
    @classmethod
    async def get_user_vocabulary(cls, db: AsyncSession, user_id: uuid.UUID, limit: int = 100) -> List[Vocabulary]:
        """
        Get vocabulary list for a specific user.
        Returns vocabulary ordered by creation date (newest first).
        """
        result = await db.execute(
            select(Vocabulary).where(Vocabulary.user_id == user_id).order_by(Vocabulary.created_at.desc()).limit(limit)
        )
        return result.scalars().all()

    @classmethod
    async def get_vocabulary_by_id(cls, db: AsyncSession, vocabulary_id: uuid.UUID) -> Optional[Vocabulary]:
        """Get a single vocabulary item by ID"""
        result = await db.execute(select(Vocabulary).where(Vocabulary.id == vocabulary_id).limit(1))
        return result.scalar_one_or_none()

    @classmethod
    async def get_vocabulary_by_word(cls, db: AsyncSession, user_id: uuid.UUID, word: str) -> Optional[Vocabulary]:
        """Get vocabulary item by word for a specific user"""
        result = await db.execute(
            select(Vocabulary).where(Vocabulary.user_id == user_id).where(Vocabulary.word == word).limit(1)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def create_vocabulary(
        cls,
        db: AsyncSession,
        user_id: uuid.UUID,
        word: str,
        source: str,
        context: Optional[str] = None,
    ) -> Vocabulary:
        """Create a new vocabulary item"""
        vocabulary = Vocabulary(
            user_id=user_id,
            word=word,
            source=source,
            notes=context,
        )

        db.add(vocabulary)
        await db.commit()
        await db.refresh(vocabulary)

        return vocabulary

    @classmethod
    async def add_vocabulary_words(
        cls,
        db: AsyncSession,
        user_id: uuid.UUID,
        words: List[str],
        source: str,
        context: Optional[str] = None,
    ) -> tuple[List[Vocabulary], int]:
        """
        Add multiple vocabulary words, skipping duplicates.
        Returns (added_words, duplicate_count)
        """
        added_words = []
        duplicate_count = 0

        for word in words:
            # Check if word already exists for this user
            existing = await cls.get_vocabulary_by_word(db, user_id, word)
            if existing:
                duplicate_count += 1
                continue

            # Create new vocabulary item
            vocabulary = await cls.create_vocabulary(db, user_id, word, source, context)
            added_words.append(vocabulary)

        return added_words, duplicate_count

    @classmethod
    async def update_vocabulary(
        cls,
        db: AsyncSession,
        vocabulary_id: uuid.UUID,
        user_id: uuid.UUID,
        reviewed: Optional[bool] = None,
        mastered: Optional[bool] = None,
        notes: Optional[str] = None,
    ) -> Optional[Vocabulary]:
        """
        Update vocabulary word status.
        Returns None if vocabulary not found or doesn't belong to user.
        """
        # Get vocabulary item and verify ownership
        vocabulary = await cls.get_vocabulary_by_id(db, vocabulary_id)
        if not vocabulary or vocabulary.user_id != user_id:
            return None

        # Update fields if provided
        if reviewed is not None:
            vocabulary.reviewed = reviewed
        if mastered is not None:
            vocabulary.mastered = mastered
        if notes is not None:
            vocabulary.notes = notes

        await db.commit()
        await db.refresh(vocabulary)

        return vocabulary

    @classmethod
    async def delete_vocabulary(
        cls,
        db: AsyncSession,
        vocabulary_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> bool:
        """
        Delete vocabulary word.
        Returns True if deleted successfully, False if not found or doesn't belong to user.
        """
        # Get vocabulary item and verify ownership
        vocabulary = await cls.get_vocabulary_by_id(db, vocabulary_id)
        if not vocabulary or vocabulary.user_id != user_id:
            return False

        # Delete the vocabulary item
        await db.delete(vocabulary)
        await db.commit()

        return True
