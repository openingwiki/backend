"""Redis database connection."""

from redis import Redis


def open_connection() -> Redis:
    """
    Opening connection session to Redis database.

    Parameters:
        Nothing

    Returns:
        database_session: Redis - Redis database session.
    """
    return Redis(host="localhost", port=6379, decode_responses=True)
