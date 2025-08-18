from typing import List

from app.model.model import Passage, PracticeQuestion
from app.schema.practice import (
    PassageResponse,
    QuestionResponse,
    ReadingPassageResponse,
    SpeakingQuestionResponse,
    WritingPromptResponse,
)


def convert_question_to_response(question: PracticeQuestion) -> QuestionResponse:
    """Convert a PracticeQuestion model to QuestionResponse"""
    # Determine question type and format response accordingly
    question_type = question.question_type.lower()

    # Handle different question types
    if question_type in ["multiple_choice", "mcq"]:
        # For multiple choice questions, options should be in the options field
        options = question.options.get("options", []) if question.options else []
        correct_index = question.options.get("correct_index") if question.options else None

        return QuestionResponse(
            id=question.id, question=question.question_text, options=options, correct=correct_index, type=question_type
        )
    else:
        # For other question types (completion, short answer, etc.)
        return QuestionResponse(
            id=question.id, question=question.question_text, answer=question.correct_answer, type=question_type
        )


def convert_passage_to_response(passage: Passage) -> PassageResponse:
    """Convert a Passage model with questions to PassageResponse"""
    questions = []
    if hasattr(passage, "questions") and passage.questions:
        questions = [convert_question_to_response(q) for q in passage.questions]

    return PassageResponse(
        id=passage.id,
        title=passage.title,
        text=passage.content,  # Map content to text field
        questions=questions,
    )


def convert_reading_passage_to_response(passage: Passage) -> ReadingPassageResponse:
    """Convert a Passage model with questions to ReadingPassageResponse"""
    questions = []
    if hasattr(passage, "questions") and passage.questions:
        questions = [convert_question_to_response(q) for q in passage.questions]

    return ReadingPassageResponse(
        id=passage.id,
        title=passage.title,
        passage=passage.content,  # Map content to passage field
        questions=questions,
    )


def convert_speaking_question_to_response(question: PracticeQuestion) -> SpeakingQuestionResponse:
    """Convert a PracticeQuestion model to SpeakingQuestionResponse"""
    # Extract speaking-specific fields from question_text or options
    # Assuming the question_text contains the question and other fields are in options
    question_text = question.question_text

    # Extract additional fields from options if available
    options = question.options or {}
    title = options.get("title", "Speaking Question")
    part = options.get("part", "Part 1")
    preparation_time = options.get("preparationTime", 60)  # Default 60 seconds

    return SpeakingQuestionResponse(
        id=question.id,
        question=question_text,
        title=title,
        part=part,
        type="speaking",
        preparationTime=preparation_time,
    )


def convert_writing_prompt_to_response(question: PracticeQuestion) -> WritingPromptResponse:
    """Convert a PracticeQuestion model to WritingPromptResponse"""
    # Extract writing-specific fields from question_text or options
    question_text = question.question_text

    # Extract additional fields from options if available
    options = question.options or {}
    title = options.get("title", "Writing Task")
    prompt_type = options.get("type", "essay")  # Default to essay
    time_limit = options.get("timeLimit", 3600)  # Default 60 minutes (3600 seconds)
    word_limit = options.get("wordLimit", "250-300 words")  # Default word limit

    return WritingPromptResponse(
        id=question.id,
        question=question_text,
        title=title,
        type=prompt_type,
        timeLimit=time_limit,
        wordLimit=word_limit,
    )
