import time
from functools import wraps

def retry(max_attempts=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"[Retry] Attempt {attempts} failed: {e}")
                    time.sleep(delay)
            raise Exception(f"[Retry] All {max_attempts} attempts failed for {func.__name__}")
        return wrapper
    return decorator
