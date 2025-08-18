from typing import Annotated, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.utils.practice import (
    convert_passage_to_response,
    convert_reading_passage_to_response,
    convert_speaking_question_to_response,
    convert_writing_prompt_to_response,
)
from app.core.depends.get_session import get_session
from app.crud.practice import PracticeCrud

router = APIRouter(
    prefix="/practice",
    tags=["practice"],
)


@router.get("/listening")
async def get_listening_practice(
    db: Annotated[AsyncSession, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    """
    Get listening practice questions
    """
    # Get listening passages with questions
    passages = await PracticeCrud.get_listening_passages_with_questions(db, limit=limit)

    # Convert to response format
    passage_responses = [convert_passage_to_response(passage) for passage in passages]

    return {"success": True, "data": {"passages": passage_responses}}


@router.get("/reading")
async def get_reading_practice(
    db: Annotated[AsyncSession, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    """
    Get reading practice questions
    """
    # Get reading passages with questions
    passages = await PracticeCrud.get_reading_passages_with_questions(db, limit=limit)

    # Convert to response format
    passage_responses = [convert_reading_passage_to_response(passage) for passage in passages]

    return {"success": True, "data": {"passages": passage_responses}}


@router.get("/speaking")
async def get_speaking_practice(
    db: Annotated[AsyncSession, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    """
    Get speaking practice questions
    """
    # Get speaking questions
    questions = await PracticeCrud.get_speaking_questions(db, limit=limit)

    # Convert to response format
    question_responses = [convert_speaking_question_to_response(question) for question in questions]

    return {"success": True, "data": {"questions": question_responses}}


@router.get("/writing")
async def get_writing_practice(
    db: Annotated[AsyncSession, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    """
    Get writing practice questions
    """
    # Get writing prompts
    prompts = await PracticeCrud.get_writing_prompts(db, limit=limit)

    # Convert to response format
    prompt_responses = [convert_writing_prompt_to_response(prompt) for prompt in prompts]

    return {"success": True, "data": {"prompts": prompt_responses}}
