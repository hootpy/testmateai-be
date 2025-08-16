from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.depends.get_current_user import get_current_user
from app.core.depends.get_session import get_session
from app.model.model import User
from app.schema.ai import (
    SpeakingFeedbackRequest,
    SpeakingFeedbackResponse,
    WritingFeedbackRequest,
    WritingFeedbackResponse,
)

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


@router.post("/writing-feedback", response_model=WritingFeedbackResponse)
async def get_writing_feedback(
    payload: WritingFeedbackRequest,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> WritingFeedbackResponse:
    """
    Process written text and provide detailed feedback on various aspects of writing
    """
    # Here you would integrate with your AI service to analyze the writing
    # For now, we'll return mock data

    # Mock implementation - in a real app, this would call an AI service
    # that processes the prompt and answer to generate feedback

    mock_response = WritingFeedbackResponse(
        band=6.5,
        comment="Your writing demonstrates a good understanding of the topic with clear organization. "
        "There are some areas for improvement in grammatical accuracy and vocabulary range.",
        task_achievement="You've addressed all parts of the task and provided relevant ideas with some supporting details. "
        "To improve, make your examples more specific and elaborate further on key points.",
        coherence_cohesion="Your essay has a clear structure with logical paragraphing. "
        "However, you could use more cohesive devices to connect ideas more smoothly.",
        lexical_resource="You use a mix of common and less common vocabulary appropriately. "
        "To reach a higher band, incorporate more precise terminology and academic phrases.",
        grammatical_range="You use a variety of sentence structures with good control. "
        "There are occasional errors in complex structures and some issues with article usage.",
        suggestions=[
            "Use more specific examples to support your main points",
            "Incorporate more academic vocabulary related to the topic",
            "Pay attention to article usage (a/an/the)",
            "Add more transition words between paragraphs",
            "Vary your sentence beginnings more",
        ],
        improved_version="The question of whether technology has improved our lives is multifaceted. On one hand, "
        "technological advancements have undoubtedly revolutionized healthcare, communication, and education. "
        "For instance, medical innovations such as MRI machines and robotic surgery have significantly enhanced "
        "diagnostic capabilities and treatment outcomes. Moreover, communication platforms enable instant "
        "connections regardless of geographical barriers, fostering both personal and professional relationships. "
        "Educational technology has similarly democratized access to knowledge through online courses and digital "
        "resources.\n\n"
        "Nevertheless, technology has introduced new challenges. The pervasiveness of social media has been "
        "linked to rising rates of mental health issues, particularly among younger generations. Furthermore, "
        "our increasing dependence on digital systems raises concerns about privacy, security, and the potential "
        "loss of traditional skills. The environmental impact of technological production and disposal also "
        "presents a significant drawback.\n\n"
        "In conclusion, while technology has brought remarkable improvements to many aspects of human life, "
        "we must acknowledge and address its downsides. A balanced approach to technological integration, "
        "coupled with thoughtful regulation and mindful usage, would enable us to maximize benefits while "
        "mitigating negative consequences.",
    )

    return mock_response
