"""
Read-only admin views for all database models.
"""
# mypy: disable-error-code="list-item"
from sqladmin import ModelView

from app.models import (
    User,
    Question,
    UserQuestion,
    TestSession,
    Response,
    TestResult,
)


class ReadOnlyModelView(ModelView):
    """
    Base class for read-only admin views.

    Disables all create, edit, and delete operations.
    """

    can_create = False
    can_edit = False
    can_delete = False
    can_export = True  # Allow data export
    page_size = 50  # Show 50 records per page
    page_size_options = [25, 50, 100, 200]


class UserAdmin(ReadOnlyModelView, model=User):
    """Admin view for User model."""

    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    # Columns to display in list view
    column_list = [
        User.id,
        User.email,
        User.first_name,
        User.last_name,
        User.created_at,
        User.last_login_at,
        User.notification_enabled,
    ]

    # Columns to show in detail view
    column_details_list = [
        User.id,
        User.email,
        User.first_name,
        User.last_name,
        User.created_at,
        User.last_login_at,
        User.notification_enabled,
        User.apns_device_token,
    ]

    # Searchable columns
    column_searchable_list = [User.email, User.first_name, User.last_name]

    # Sortable columns
    column_sortable_list = [User.id, User.email, User.created_at, User.last_login_at]

    # Default sort order
    column_default_sort = [(User.created_at, True)]  # Descending order


class QuestionAdmin(ReadOnlyModelView, model=Question):
    """Admin view for Question model."""

    name = "Question"
    name_plural = "Questions"
    icon = "fa-solid fa-question"

    column_list = [
        Question.id,
        Question.question_type,
        Question.difficulty_level,
        Question.source_llm,
        Question.arbiter_score,
        Question.created_at,
        Question.is_active,
    ]

    column_details_list = [
        Question.id,
        Question.question_text,
        Question.question_type,
        Question.difficulty_level,
        Question.correct_answer,
        Question.answer_options,
        Question.explanation,
        Question.question_metadata,
        Question.source_llm,
        Question.arbiter_score,
        Question.created_at,
        Question.is_active,
    ]

    column_searchable_list = [Question.question_text, Question.source_llm]

    column_sortable_list = [
        Question.id,
        Question.question_type,
        Question.difficulty_level,
        Question.arbiter_score,
        Question.created_at,
    ]

    column_default_sort = [(Question.created_at, True)]

    # Add filters for common queries
    column_filters = [
        Question.question_type,
        Question.difficulty_level,
        Question.is_active,
        Question.source_llm,
    ]


class UserQuestionAdmin(ReadOnlyModelView, model=UserQuestion):
    """Admin view for UserQuestion junction table."""

    name = "User Question"
    name_plural = "User Questions"
    icon = "fa-solid fa-link"

    column_list = [
        UserQuestion.id,
        UserQuestion.user_id,
        UserQuestion.question_id,
        UserQuestion.seen_at,
    ]

    column_sortable_list = [
        UserQuestion.id,
        UserQuestion.user_id,
        UserQuestion.question_id,
        UserQuestion.seen_at,
    ]

    column_default_sort = [(UserQuestion.seen_at, True)]

    column_filters = [UserQuestion.user_id, UserQuestion.question_id]


class TestSessionAdmin(ReadOnlyModelView, model=TestSession):
    """Admin view for TestSession model."""

    name = "Test Session"
    name_plural = "Test Sessions"
    icon = "fa-solid fa-clipboard"

    column_list = [
        TestSession.id,
        TestSession.user_id,
        TestSession.started_at,
        TestSession.completed_at,
        TestSession.status,
    ]

    column_sortable_list = [
        TestSession.id,
        TestSession.user_id,
        TestSession.started_at,
        TestSession.completed_at,
    ]

    column_default_sort = [(TestSession.started_at, True)]

    column_filters = [TestSession.user_id, TestSession.status]


class ResponseAdmin(ReadOnlyModelView, model=Response):
    """Admin view for Response model."""

    name = "Response"
    name_plural = "Responses"
    icon = "fa-solid fa-reply"

    column_list = [
        Response.id,
        Response.test_session_id,
        Response.user_id,
        Response.question_id,
        Response.is_correct,
        Response.answered_at,
    ]

    column_details_list = [
        Response.id,
        Response.test_session_id,
        Response.user_id,
        Response.question_id,
        Response.user_answer,
        Response.is_correct,
        Response.answered_at,
    ]

    column_sortable_list = [
        Response.id,
        Response.test_session_id,
        Response.user_id,
        Response.question_id,
        Response.answered_at,
    ]

    column_default_sort = [(Response.answered_at, True)]

    column_filters = [
        Response.test_session_id,
        Response.user_id,
        Response.question_id,
        Response.is_correct,
    ]


class TestResultAdmin(ReadOnlyModelView, model=TestResult):
    """Admin view for TestResult model."""

    name = "Test Result"
    name_plural = "Test Results"
    icon = "fa-solid fa-chart-line"

    column_list = [
        TestResult.id,
        TestResult.test_session_id,
        TestResult.user_id,
        TestResult.iq_score,
        TestResult.total_questions,
        TestResult.correct_answers,
        TestResult.completion_time_seconds,
        TestResult.completed_at,
    ]

    column_sortable_list = [
        TestResult.id,
        TestResult.user_id,
        TestResult.iq_score,
        TestResult.completed_at,
    ]

    column_default_sort = [(TestResult.completed_at, True)]

    column_filters = [TestResult.user_id, TestResult.iq_score]
