from redis import Redis


def delete_if_keys_exists(redis: Redis, pattern: str) -> None:
    list_keys = redis.keys(pattern)

    if list_keys:
        redis.delete(*list_keys)
