from sqlalchemy.orm import Session

from app.core import security, settings
from app.crud import crud_user
from app.db.session import Base, engine  # noqa: F401
from app.schemas import UserCreate


def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)

    user = crud_user.get_by_email(db, email=settings.FIRST_ADMIN_EMAIL)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_ADMIN_EMAIL,
            nickname=settings.FIRST_ADMIN_NICKNAME,
            hashed_password=security.get_password_hash(settings.FIRST_ADMIN_PASSWORD),
        )
        user = crud_user.create(db, user_in)
        crud_user.verify(db, user)
        crud_user.set_moderator(db, user)
