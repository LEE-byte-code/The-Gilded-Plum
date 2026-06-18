import time
from functools import wraps
from django.http import JsonResponse
from django.core.cache import cache


def rate_limit(key_prefix, max_requests=10, window=60):
    """Rate-limit a view by client IP.

    Usage:
        @rate_limit('book', max_requests=5, window=60)
        def my_view(request): ...

    Allows `max_requests` requests per `window` seconds per IP.
    """
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            ip = request.META.get('REMOTE_ADDR', 'unknown')
            cache_key = f'ratelimit:{key_prefix}:{ip}'
            now = time.time()

            history = cache.get(cache_key, [])
            history = [t for t in history if t > now - window]

            if len(history) >= max_requests:
                retry_after = int(history[0] + window - now) if history else window
                return JsonResponse(
                    {'error': f'Too many requests. Try again in {retry_after} seconds.'},
                    status=429,
                    headers={'Retry-After': str(retry_after)},
                )

            history.append(now)
            cache.set(cache_key, history, timeout=window)
            return view(request, *args, **kwargs)
        return wrapper
    return decorator
