from typing import List

from app.model.model import MockTest
from app.schema.mock_test import MockTestResponse, MockTestSectionResponse


def convert_mock_test_to_response(mock_test: MockTest) -> MockTestResponse:
    """Convert a MockTest model to MockTestResponse"""
    # Convert sections from JSONB to list of MockTestSectionResponse
    sections = []
    if mock_test.sections:
        for section in mock_test.sections:
            sections.append(
                MockTestSectionResponse(
                    id=section.get("id", ""),
                    name=section.get("name", ""),
                    time=section.get("time", ""),
                    questions=section.get("questions", 0),
                )
            )

    return MockTestResponse(
        id=mock_test.id,
        name=mock_test.name,
        description=mock_test.description or "",
        duration=mock_test.duration,
        sections=sections,
        createdAt=mock_test.created_at,
    )
