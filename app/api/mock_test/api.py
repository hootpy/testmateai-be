import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.utils.mock_test import convert_mock_test_to_response
from app.core.depends.get_session import get_session
from app.crud.mock_test import MockTestCrud

router = APIRouter(
    prefix="/mock-tests",
    tags=["mock-tests"],
)


@router.get("")
async def get_mock_tests(
    db: Annotated[AsyncSession, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
):
    """
    Get all available mock tests
    """
    # Get all mock tests
    mock_tests = await MockTestCrud.get_all_mock_tests(db, limit=limit)

    # Convert to response format
    test_responses = [convert_mock_test_to_response(test) for test in mock_tests]

    return {"success": True, "data": test_responses}


@router.get("/{test_id}")
async def get_mock_test_by_id(
    test_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Get specific mock test details
    """
    # Get mock test by ID
    mock_test = await MockTestCrud.get_mock_test_by_id(db, test_id)

    if not mock_test:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Mock test not found")

    # Convert to response format
    test_response = convert_mock_test_to_response(mock_test)

    return {"success": True, "data": test_response}
