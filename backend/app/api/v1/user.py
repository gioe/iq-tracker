"""
User profile endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models import get_db, User
from app.schemas.auth import UserResponse, UserProfileUpdate
from app.core.auth import get_current_user

router = APIRouter()


@router.get("/profile", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user's profile information.

    Args:
        current_user: Current authenticated user

    Returns:
        User profile information
    """
    return current_user


@router.put("/profile", response_model=UserResponse)
def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update current user's profile information.

    Only provided fields will be updated. Fields not included in the
    request body will remain unchanged.

    Args:
        profile_update: Profile fields to update
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated user profile information
    """
    # Update only provided fields
    update_data = profile_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user
