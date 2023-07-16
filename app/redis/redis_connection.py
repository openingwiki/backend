from redis import Redis


def open_connection() -> Redis:
    return Redis(host='localhost', port=6379, decode_responses=True)