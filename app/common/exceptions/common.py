from fastapi import HTTPException
from starlette import status


class UniqueViolationField(HTTPException):
    """Exception to be raised when unique constraint is violated."""

    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Unique constraint violation")
