from functools import wraps
from .redis_cache import RedisCache

def fetch_from_cache(cache_name: str, cache_config: dict):
    cache_conn = RedisCache(cache_config['redis'])
    ttl = cache_config['ttl']

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cached_value = cache_conn.get(cache_name)
            print('cached_value', cached_value)
            if cached_value:
                return cached_value
            response = func(*args, **kwargs)
            print('response', response)
            cache_conn.set(cache_name, response, ttl)
            return response
        return wrapper
    return decorator