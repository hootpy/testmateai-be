from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.depends.get_current_user import get_current_user
from app.core.depends.get_session import get_session
from app.model.model import User
from app.schema.ai import (
    FocusArea,
    SpeakingFeedbackRequest,
    SpeakingFeedbackResponse,
    StudyPlanRequest,
    StudyPlanResponse,
    WeeklyTask,
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


@router.post("/study-plan", response_model=StudyPlanResponse)
async def generate_study_plan(
    payload: StudyPlanRequest,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> StudyPlanResponse:
    """
    Generate a personalized study plan based on current score, target score, test date, and available time
    """
    # Calculate number of weeks until test date
    today = datetime.now().date()
    weeks_until_test = max(1, (payload.testDate - today).days // 7)

    # Here you would integrate with your AI service to generate a customized study plan
    # For now, we'll return mock data that scales based on the input parameters

    # Dynamically adjust study intensity based on score gap and available time
    score_gap = payload.targetScore - payload.currentScore
    intensity_factor = min(1.0, (score_gap / 2.0) * (payload.availableTime / 120))

    # Generate focus areas based on the score gap
    focus_areas = []

    if score_gap >= 0.5:
        # Prioritize different skills based on the gap size
        if score_gap >= 2.0:
            # For large gaps, focus on all areas with priorities
            focus_areas = [
                FocusArea(
                    skill="Listening",
                    reason="Your current performance indicates significant room for improvement in understanding different accents and complex information.",
                    priority=1,
                ),
                FocusArea(
                    skill="Reading",
                    reason="You need to build stronger skimming and scanning techniques to improve comprehension speed and accuracy.",
                    priority=2,
                ),
                FocusArea(
                    skill="Writing",
                    reason="Focus on essay structure and coherence to improve your written responses.",
                    priority=3,
                ),
                FocusArea(
                    skill="Speaking",
                    reason="Work on fluency and pronunciation to express ideas more clearly.",
                    priority=4,
                ),
            ]
        elif score_gap >= 1.0:
            # For medium gaps, focus on key areas
            focus_areas = [
                FocusArea(
                    skill="Writing",
                    reason="Your writing organization and vocabulary range need improvement to reach your target score.",
                    priority=1,
                ),
                FocusArea(
                    skill="Speaking",
                    reason="Practice speaking with more complex grammatical structures and better pronunciation.",
                    priority=2,
                ),
                FocusArea(
                    skill="Reading",
                    reason="Enhance your ability to identify main ideas and supporting details.",
                    priority=3,
                ),
            ]
        else:
            # For small gaps, focus on refinement
            focus_areas = [
                FocusArea(
                    skill="Speaking",
                    reason="Refine your speaking to include more academic vocabulary and complex structures.",
                    priority=1,
                ),
                FocusArea(
                    skill="Writing",
                    reason="Focus on advanced writing techniques to boost your score to the target level.",
                    priority=2,
                ),
            ]

    # Generate weekly schedule
    weekly_schedule = []

    for week in range(1, min(weeks_until_test + 1, 13)):  # Cap at 12 weeks
        if week <= 4:
            # First month: focus on fundamentals
            focus = "Building core skills"
            tasks = [
                f"Complete {int(30 * intensity_factor)} reading practice questions",
                f"Listen to {int(5 * intensity_factor)} academic lectures and take notes",
                f"Write {int(2 * intensity_factor)} practice essays and review them",
                f"Practice speaking for {int(20 * intensity_factor)} minutes daily with recorded responses",
            ]
        elif week <= 8:
            # Second month: practice and strategy
            focus = "Test strategies and practice"
            tasks = [
                f"Take {int(2 * intensity_factor)} full-length practice tests",
                "Review mistakes and identify pattern errors",
                "Practice time management during reading and listening sections",
                "Work on specific vocabulary for your weak areas",
            ]
        else:
            # Final weeks: refinement and full tests
            focus = "Refinement and full test preparation"
            tasks = [
                "Complete one full practice test per week",
                "Focus on your highest priority skill areas",
                "Review all vocabulary and grammar notes",
                "Practice stress management and test day strategies",
            ]

        weekly_schedule.append(WeeklyTask(week=week, focus=focus, tasks=tasks))

    # Generate general recommendations
    recommendations = [
        f"Study at least {payload.availableTime} minutes every day",
        "Focus on your weakest skills first",
        "Track your progress with regular practice tests",
        "Use official test preparation materials",
        "Consider joining a study group or finding a study partner",
    ]

    if payload.availableTime < 60:
        recommendations.append("Try to increase your daily study time to at least 60 minutes for better results")

    if weeks_until_test < 4:
        recommendations.append(
            "Your test date is very soon. Consider intensive preparation or rescheduling if possible"
        )

    # Create summary based on all factors
    summary = f"This {weeks_until_test}-week study plan will help you improve from band {payload.currentScore} to your target of {payload.targetScore}. "

    if score_gap > 2.0:
        summary += "The gap between your current and target scores is significant, requiring dedicated daily study. "
    elif score_gap > 1.0:
        summary += "You'll need consistent effort to bridge the gap to your target score. "
    else:
        summary += "With focused practice on key areas, your target score is achievable. "

    if weeks_until_test < 8:
        summary += f"With {weeks_until_test} weeks until your test, you should begin your preparation immediately."
    else:
        summary += f"You have {weeks_until_test} weeks to prepare, which gives you sufficient time if you follow this plan consistently."

    # Construct and return the response
    mock_response = StudyPlanResponse(
        summary=summary,
        weeks=min(weeks_until_test, 12),  # Cap at 12 weeks in the plan
        recommendations=recommendations,
        weekly_schedule=weekly_schedule,
        focus_areas=focus_areas,
    )

    return mock_response
