from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.depends.get_current_user import get_current_user
from app.core.depends.get_session import get_session
from app.model.model import User
from app.schema.ai import SpeakingFeedbackRequest, SpeakingFeedbackResponse

router = APIRouter(
    prefix="/ai",
    tags=["ai"],
)


@router.post("/speaking-feedback", response_model=SpeakingFeedbackResponse)
async def get_speaking_feedback(
    payload: SpeakingFeedbackRequest,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> SpeakingFeedbackResponse:
    """
    Process speech audio and provide detailed feedback
    """
    # Here you would integrate with your AI service to analyze the speech
    # For now, we'll return mock data

    # Mock implementation - in a real app, this would call an AI service
    # that processes the audio and transcript to generate feedback

    mock_response = SpeakingFeedbackResponse(
        band=6.5,
        comment="Overall, your speaking demonstrates good fluency and reasonable vocabulary usage. "
        "Focus on improving grammatical accuracy and pronunciation of key terms.",
        words=[
            {
                "word": "environment",
                "native_like": False,
                "score": 0.6,
                "tip": "Focus on pronouncing all syllables clearly: en-vai-ruh-ment",
            },
            {"word": "technology", "native_like": True, "score": 0.9, "tip": None},
            {
                "word": "development",
                "native_like": False,
                "score": 0.7,
                "tip": "Pay attention to the stress on the second syllable: de-VE-lop-ment",
            },
        ],
        length_feedback="Your response was an appropriate length for this question type.",
        suggestions=[
            "Try to use more complex sentence structures",
            "Include more specific examples to support your points",
        ],
        pronunciation_tips=[
            "Practice the 'th' sound in words like 'think' and 'therefore'",
            "Pay attention to word stress in multisyllabic words",
        ],
        grammar_feedback="You sometimes mix present and past tenses. Try to maintain consistent tense usage throughout your response.",
        vocabulary_feedback="You used a good range of vocabulary, but could incorporate more academic terms related to the topic.",
        coherence_feedback="Your ideas flow logically, but adding more transition phrases would improve coherence between different points.",
    )

    return mock_response
