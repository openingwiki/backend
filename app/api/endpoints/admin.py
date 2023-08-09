"""
Requests which can be made only by admin.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_user
from app.models import User

from .. import dependencies

router = APIRouter()


@router.put(path="/set_moderator/{id}", description="Setting moderator status to user.")
async def set_moderator(
    id: int, db: Session = Depends(dependencies.get_db), admin: User = Depends(dependencies.get_current_admin)
):
    """
    Setting moderator status to user.

    Parameters:
        id: int - if of user to set moderator
        db: Session - SQLAlchemy session to database, initializing in dependency injection.
        user: User - user sqlalchemy model, dependency injection gets access token from cookie.

    Raises:
        HTTPException(403) - invalid user id.

    Returns:
        Muda JSON.
    """
    user_to_moderator = crud_user.get(db, id)

    if not user_to_moderator:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="There is not such user.")

    crud_user.set_moderator(db, user_to_moderator)

    return {"message": "user is a moderator now."}
