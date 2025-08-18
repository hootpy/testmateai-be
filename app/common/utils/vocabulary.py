from typing import List

from app.model.model import Vocabulary
from app.schema.vocabulary import VocabularyResponse


def convert_vocabulary_to_response(vocabulary: Vocabulary) -> VocabularyResponse:
    """Convert a Vocabulary model to VocabularyResponse"""
    return VocabularyResponse(
        id=vocabulary.id,
        word=vocabulary.word,
        definition=vocabulary.definition,
        source=vocabulary.source,
        reviewed=vocabulary.reviewed,
        mastered=vocabulary.mastered,
        notes=vocabulary.notes,
        createdAt=vocabulary.created_at,
    )


def convert_vocabulary_to_added_response(vocabulary: Vocabulary) -> dict:
    """Convert a Vocabulary model to AddedVocabularyResponse format"""
    return {
        "id": vocabulary.id,
        "word": vocabulary.word,
        "source": vocabulary.source,
        "createdAt": vocabulary.created_at,
    }


def convert_vocabulary_to_update_response(vocabulary: Vocabulary) -> dict:
    """Convert a Vocabulary model to UpdateVocabularyResponse format"""
    return {
        "id": vocabulary.id,
        "word": vocabulary.word,
        "reviewed": vocabulary.reviewed,
        "mastered": vocabulary.mastered,
        "notes": vocabulary.notes,
        "updatedAt": vocabulary.created_at,  # Using created_at as updatedAt since no updated_at field
    }
