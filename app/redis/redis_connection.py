"""Redis database connection."""

from redis import Redis

from app.core.config import settings


def open_connection() -> Redis:
    """
    Opening connection session to Redis database.

    Parameters:
        Nothing

    Returns:
        database_session: Redis - Redis database session.
    """
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
