import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.utils.vocabulary import (
    convert_vocabulary_to_added_response,
    convert_vocabulary_to_response,
    convert_vocabulary_to_update_response,
)
from app.core.depends.get_current_user import get_current_user
from app.core.depends.get_session import get_session
from app.crud.vocabulary import VocabularyCrud
from app.model.model import User
from app.schema.vocabulary import AddVocabularyRequest, UpdateVocabularyRequest

router = APIRouter(
    prefix="/vocabulary",
    tags=["vocabulary"],
)


@router.get("")
async def get_user_vocabulary(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
):
    """
    Get user's vocabulary list
    """
    # Get user vocabulary
    vocabulary_list = await VocabularyCrud.get_user_vocabulary(db, current_user.id, limit=limit)

    # Convert to response format
    vocabulary_responses = [convert_vocabulary_to_response(vocab) for vocab in vocabulary_list]

    return {"success": True, "data": vocabulary_responses}


@router.post("")
async def add_vocabulary_words(
    payload: AddVocabularyRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Add new vocabulary words
    """
    # Validate source
    valid_sources = ["practice", "mock_test", "manual"]
    if payload.source not in valid_sources:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid source. Must be one of: {', '.join(valid_sources)}",
        )

    # Validate words array is not empty
    if not payload.words:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Words array cannot be empty",
        )

    # Add vocabulary words
    added_words, duplicate_count = await VocabularyCrud.add_vocabulary_words(
        db=db,
        user_id=current_user.id,
        words=payload.words,
        source=payload.source,
        context=payload.context,
    )

    # Convert to response format
    words_response = [convert_vocabulary_to_added_response(word) for word in added_words]

    return {
        "success": True,
        "data": {"addedWords": len(added_words), "duplicateWords": duplicate_count, "words": words_response},
        "message": "Vocabulary words added successfully",
    }


@router.put("/{word_id}")
async def update_vocabulary_word(
    word_id: uuid.UUID,
    payload: UpdateVocabularyRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Update vocabulary word status
    """
    # Validate that at least one field is provided
    if payload.reviewed is None and payload.mastered is None and payload.notes is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (reviewed, mastered, or notes) must be provided",
        )

    # Update vocabulary word
    updated_vocabulary = await VocabularyCrud.update_vocabulary(
        db=db,
        vocabulary_id=word_id,
        user_id=current_user.id,
        reviewed=payload.reviewed,
        mastered=payload.mastered,
        notes=payload.notes,
    )

    if not updated_vocabulary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vocabulary word not found or you don't have permission to update it",
        )

    # Convert to response format
    vocabulary_response = convert_vocabulary_to_update_response(updated_vocabulary)

    return {"success": True, "data": vocabulary_response, "message": "Vocabulary word updated successfully"}


@router.delete("/{word_id}")
async def delete_vocabulary_word(
    word_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Remove vocabulary word
    """
    # Delete vocabulary word
    deleted = await VocabularyCrud.delete_vocabulary(
        db=db,
        vocabulary_id=word_id,
        user_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vocabulary word not found or you don't have permission to delete it",
        )

    return {"success": True, "message": "Vocabulary word removed successfully"}
