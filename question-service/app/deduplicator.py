"""Question deduplication checking.

This module provides functionality to detect duplicate questions using both
exact match checking and semantic similarity analysis via embeddings.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from openai import OpenAI

from .models import GeneratedQuestion

logger = logging.getLogger(__name__)


class DuplicateCheckResult:
    """Result of a duplicate check operation.

    Attributes:
        is_duplicate: Whether the question is a duplicate
        duplicate_type: Type of duplicate ("exact" or "semantic")
        similarity_score: Similarity score (1.0 for exact, 0.0-1.0 for semantic)
        matched_question: The matched question data if duplicate found
    """

    def __init__(
        self,
        is_duplicate: bool,
        duplicate_type: Optional[str] = None,
        similarity_score: float = 0.0,
        matched_question: Optional[Dict[str, Any]] = None,
    ):
        """Initialize duplicate check result.

        Args:
            is_duplicate: Whether question is a duplicate
            duplicate_type: Type of duplicate detection
            similarity_score: Similarity score
            matched_question: Matched question data
        """
        self.is_duplicate = is_duplicate
        self.duplicate_type = duplicate_type
        self.similarity_score = similarity_score
        self.matched_question = matched_question

    def __repr__(self) -> str:
        """String representation of result."""
        if not self.is_duplicate:
            return "DuplicateCheckResult(is_duplicate=False)"
        return (
            f"DuplicateCheckResult(is_duplicate=True, type={self.duplicate_type}, "
            f"score={self.similarity_score:.3f})"
        )


class QuestionDeduplicator:
    """Checks for duplicate questions using exact and semantic matching.

    This class provides methods to detect duplicate questions by comparing
    question text using both exact string matching and semantic similarity
    via embeddings.
    """

    def __init__(
        self,
        openai_api_key: str,
        similarity_threshold: float = 0.85,
        embedding_model: str = "text-embedding-3-small",
    ):
        """Initialize the question deduplicator.

        Args:
            openai_api_key: OpenAI API key for embeddings
            similarity_threshold: Threshold for semantic similarity (0.0-1.0)
            embedding_model: OpenAI embedding model to use

        Raises:
            ValueError: If similarity_threshold is not between 0 and 1
        """
        if not 0.0 <= similarity_threshold <= 1.0:
            raise ValueError(
                f"similarity_threshold must be between 0.0 and 1.0, got {similarity_threshold}"
            )

        self.openai_client = OpenAI(api_key=openai_api_key)
        self.similarity_threshold = similarity_threshold
        self.embedding_model = embedding_model

        logger.info(
            f"QuestionDeduplicator initialized with threshold={similarity_threshold}, "
            f"model={embedding_model}"
        )

    def check_duplicate(
        self,
        question: GeneratedQuestion,
        existing_questions: List[Dict[str, Any]],
    ) -> DuplicateCheckResult:
        """Check if a question is a duplicate of any existing questions.

        Args:
            question: Generated question to check
            existing_questions: List of existing question data dictionaries
                               Each should have 'question_text' key

        Returns:
            DuplicateCheckResult with duplicate status and details

        Raises:
            Exception: If embedding generation fails
        """
        question_text = question.question_text.strip().lower()

        # Step 1: Check for exact match (case-insensitive)
        for existing in existing_questions:
            existing_text = existing.get("question_text", "").strip().lower()
            if question_text == existing_text:
                logger.info(f"Exact duplicate found for: {question_text[:50]}...")
                return DuplicateCheckResult(
                    is_duplicate=True,
                    duplicate_type="exact",
                    similarity_score=1.0,
                    matched_question=existing,
                )

        # Step 2: Check for semantic similarity using embeddings
        if len(existing_questions) > 0:
            result = self._check_semantic_similarity(question_text, existing_questions)
            if result.is_duplicate:
                logger.info(
                    f"Semantic duplicate found with score {result.similarity_score:.3f}"
                )
                return result

        # No duplicate found
        logger.debug(f"No duplicate found for: {question_text[:50]}...")
        return DuplicateCheckResult(is_duplicate=False)

    def check_duplicates_batch(
        self,
        questions: List[GeneratedQuestion],
        existing_questions: List[Dict[str, Any]],
    ) -> List[DuplicateCheckResult]:
        """Check multiple questions for duplicates.

        Args:
            questions: List of generated questions to check
            existing_questions: List of existing question data

        Returns:
            List of DuplicateCheckResult, one per input question

        Raises:
            Exception: If any check fails
        """
        logger.info(f"Checking {len(questions)} questions for duplicates")

        results = []
        for question in questions:
            try:
                result = self.check_duplicate(question, existing_questions)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to check duplicate for question: {str(e)}")
                # Return non-duplicate result to be safe (don't block question)
                results.append(DuplicateCheckResult(is_duplicate=False))

        duplicates_found = sum(1 for r in results if r.is_duplicate)
        logger.info(
            f"Duplicate check complete: {duplicates_found}/{len(questions)} duplicates found"
        )

        return results

    def _check_semantic_similarity(
        self,
        question_text: str,
        existing_questions: List[Dict[str, Any]],
    ) -> DuplicateCheckResult:
        """Check semantic similarity using embeddings.

        Args:
            question_text: Question text to check
            existing_questions: List of existing question data

        Returns:
            DuplicateCheckResult with semantic similarity details

        Raises:
            Exception: If embedding generation fails
        """
        try:
            # Generate embedding for new question
            new_embedding = self._get_embedding(question_text)

            # Compare with existing questions
            max_similarity = 0.0
            most_similar_question = None

            for existing in existing_questions:
                existing_text = existing.get("question_text", "")
                if not existing_text:
                    continue

                # Generate embedding for existing question
                existing_embedding = self._get_embedding(existing_text)

                # Calculate cosine similarity
                similarity = self._cosine_similarity(new_embedding, existing_embedding)

                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_question = existing

            # Check if similarity exceeds threshold
            if max_similarity >= self.similarity_threshold:
                return DuplicateCheckResult(
                    is_duplicate=True,
                    duplicate_type="semantic",
                    similarity_score=max_similarity,
                    matched_question=most_similar_question,
                )

            return DuplicateCheckResult(is_duplicate=False)

        except Exception as e:
            logger.error(f"Semantic similarity check failed: {str(e)}")
            raise

    def _get_embedding(self, text: str) -> np.ndarray:
        """Generate embedding vector for text using OpenAI API.

        Args:
            text: Text to generate embedding for

        Returns:
            Numpy array containing embedding vector

        Raises:
            Exception: If API call fails
        """
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model=self.embedding_model,
            )
            embedding = response.data[0].embedding
            return np.array(embedding)

        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            raise

    def _cosine_similarity(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors.

        Args:
            vector1: First embedding vector
            vector2: Second embedding vector

        Returns:
            Cosine similarity score (0.0 to 1.0)
        """
        # Normalize vectors
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        # Calculate cosine similarity
        similarity = np.dot(vector1, vector2) / (norm1 * norm2)

        # Clamp to [0, 1] range (cosine similarity is [-1, 1], but we expect [0, 1])
        return float(max(0.0, min(1.0, similarity)))

    def filter_duplicates(
        self,
        questions: List[GeneratedQuestion],
        existing_questions: List[Dict[str, Any]],
    ) -> Tuple[
        List[GeneratedQuestion], List[Tuple[GeneratedQuestion, DuplicateCheckResult]]
    ]:
        """Filter out duplicate questions from a list.

        Args:
            questions: List of generated questions to filter
            existing_questions: List of existing question data

        Returns:
            Tuple of (unique_questions, duplicate_questions_with_results)

        Raises:
            Exception: If duplicate checking fails
        """
        logger.info(f"Filtering duplicates from {len(questions)} questions")

        unique_questions = []
        duplicates = []

        for question in questions:
            result = self.check_duplicate(question, existing_questions)

            if result.is_duplicate:
                duplicates.append((question, result))
            else:
                unique_questions.append(question)

        logger.info(
            f"Filtering complete: {len(unique_questions)} unique, "
            f"{len(duplicates)} duplicates"
        )

        return unique_questions, duplicates

    def get_stats(self) -> Dict[str, Any]:
        """Get deduplicator configuration statistics.

        Returns:
            Dictionary with configuration information
        """
        return {
            "similarity_threshold": self.similarity_threshold,
            "embedding_model": self.embedding_model,
        }
