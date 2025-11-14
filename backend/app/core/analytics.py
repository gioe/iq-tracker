"""
Analytics and event tracking for monitoring user actions and system events.
"""
import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    """Analytics event types."""

    # Authentication events
    USER_REGISTERED = "user.registered"
    USER_LOGIN = "user.login"
    USER_LOGOUT = "user.logout"
    TOKEN_REFRESHED = "user.token_refreshed"

    # Test session events
    TEST_STARTED = "test.started"
    TEST_COMPLETED = "test.completed"
    TEST_ABANDONED = "test.abandoned"
    TEST_RESUMED = "test.resumed"

    # Question events
    QUESTION_ANSWERED = "question.answered"
    QUESTION_SKIPPED = "question.skipped"

    # Notification events
    NOTIFICATION_SENT = "notification.sent"
    NOTIFICATION_DELIVERED = "notification.delivered"
    NOTIFICATION_FAILED = "notification.failed"

    # Performance events
    SLOW_REQUEST = "performance.slow_request"
    API_ERROR = "api.error"

    # Security events
    RATE_LIMIT_EXCEEDED = "security.rate_limit_exceeded"
    INVALID_TOKEN = "security.invalid_token"
    AUTH_FAILED = "security.auth_failed"


class AnalyticsTracker:
    """
    Analytics event tracker for logging and monitoring user actions.

    In production, this can be extended to send events to external
    analytics platforms (e.g., Mixpanel, Amplitude, PostHog, etc.)
    """

    @staticmethod
    def track_event(
        event_type: EventType,
        user_id: Optional[int] = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Track an analytics event.

        Args:
            event_type: Type of event being tracked
            user_id: Optional user ID associated with the event
            properties: Optional dictionary of event properties

        Example:
            AnalyticsTracker.track_event(
                EventType.TEST_COMPLETED,
                user_id=123,
                properties={"iq_score": 125, "duration_seconds": 1200}
            )
        """
        event_data = {
            "event": event_type.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id,
            "properties": properties or {},
            "environment": settings.ENV,
        }

        # Log the event
        logger.info(
            f"Analytics Event: {event_type.value}",
            extra={
                "event_data": event_data,
                "user_id": user_id,
            },
        )

        # In production, send to external analytics service
        if settings.ENV == "production":
            # TODO: Integrate with external analytics service
            # Example: mixpanel.track(user_id, event_type.value, properties)
            pass

    @staticmethod
    def track_user_registered(user_id: int, email: str) -> None:
        """Track user registration event."""
        AnalyticsTracker.track_event(
            EventType.USER_REGISTERED,
            user_id=user_id,
            properties={"email": email},
        )

    @staticmethod
    def track_user_login(user_id: int, email: str) -> None:
        """Track user login event."""
        AnalyticsTracker.track_event(
            EventType.USER_LOGIN,
            user_id=user_id,
            properties={"email": email},
        )

    @staticmethod
    def track_test_started(user_id: int, session_id: int, question_count: int) -> None:
        """Track test session start."""
        AnalyticsTracker.track_event(
            EventType.TEST_STARTED,
            user_id=user_id,
            properties={
                "session_id": session_id,
                "question_count": question_count,
            },
        )

    @staticmethod
    def track_test_completed(
        user_id: int,
        session_id: int,
        iq_score: int,
        duration_seconds: Optional[int] = None,
        accuracy: float = 0.0,
    ) -> None:
        """Track test completion."""
        AnalyticsTracker.track_event(
            EventType.TEST_COMPLETED,
            user_id=user_id,
            properties={
                "session_id": session_id,
                "iq_score": iq_score,
                "duration_seconds": duration_seconds,
                "accuracy_percentage": accuracy,
            },
        )

    @staticmethod
    def track_test_abandoned(
        user_id: int, session_id: int, answered_count: int
    ) -> None:
        """Track test abandonment."""
        AnalyticsTracker.track_event(
            EventType.TEST_ABANDONED,
            user_id=user_id,
            properties={
                "session_id": session_id,
                "answered_count": answered_count,
            },
        )

    @staticmethod
    def track_slow_request(
        method: str, path: str, duration_seconds: float, status_code: int
    ) -> None:
        """Track slow API request."""
        AnalyticsTracker.track_event(
            EventType.SLOW_REQUEST,
            properties={
                "method": method,
                "path": path,
                "duration_seconds": duration_seconds,
                "status_code": status_code,
            },
        )

    @staticmethod
    def track_api_error(
        method: str,
        path: str,
        error_type: str,
        error_message: str,
        user_id: Optional[int] = None,
    ) -> None:
        """Track API error."""
        AnalyticsTracker.track_event(
            EventType.API_ERROR,
            user_id=user_id,
            properties={
                "method": method,
                "path": path,
                "error_type": error_type,
                "error_message": error_message,
            },
        )

    @staticmethod
    def track_rate_limit_exceeded(
        user_identifier: str, endpoint: str, limit: int
    ) -> None:
        """Track rate limit violation."""
        AnalyticsTracker.track_event(
            EventType.RATE_LIMIT_EXCEEDED,
            properties={
                "user_identifier": user_identifier,
                "endpoint": endpoint,
                "limit": limit,
            },
        )


# Convenience alias
track = AnalyticsTracker.track_event
