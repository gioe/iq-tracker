"""
Main FastAPI application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import settings
from app.api.v1.api import api_router

# OpenAPI tags metadata
tags_metadata = [
    {
        "name": "health",
        "description": "Health check endpoints for monitoring application status",
    },
    {
        "name": "auth",
        "description": "Authentication endpoints for user registration, login, and token management",
    },
    {
        "name": "user",
        "description": "User profile management endpoints",
    },
    {
        "name": "questions",
        "description": "Question retrieval endpoints for fetching unseen IQ test questions",
    },
    {
        "name": "test",
        "description": "Test session management, response submission, and results retrieval endpoints",
    },
]


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "**IQ Tracker API** - A backend service for tracking cognitive performance over time.\n\n"
            "This API provides:\n"
            "* User authentication and profile management\n"
            "* Periodic IQ testing with AI-generated questions\n"
            "* Test session management and response submission\n"
            "* Historical test results and trend analysis\n\n"
            "## Authentication\n\n"
            "Most endpoints require authentication using JWT Bearer tokens. "
            "Obtain tokens via the `/v1/auth/login` endpoint.\n\n"
            "## Testing Cadence\n\n"
            "Users are recommended to take tests every 6 months for optimal cognitive tracking."
        ),
        contact={
            "name": "IQ Tracker Support",
            "email": "support@iqtracker.example.com",
        },
        license_info={
            "name": "MIT",
        },
        docs_url=f"{settings.API_V1_PREFIX}/docs",
        redoc_url=f"{settings.API_V1_PREFIX}/redoc",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        openapi_tags=tags_metadata,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_application()


@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": f"{settings.API_V1_PREFIX}/docs",
    }
