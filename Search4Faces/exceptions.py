from typing import Callable
from functools import wraps


class SearchAPIError(Exception):
    
    def __init__(self, error: dict) -> None:

        super().__init__(
            '[%(code)s] API Exception: %(message)s' % error,
        )


def check_for_errors(func: Callable) -> Callable:

    @wraps(func)
    def wrapper(*args, **kwargs) -> dict:

        response = func(*args, **kwargs)

        if 'error' in response:

            raise SearchAPIError(response['error'])

        return response

    return wrapper


def check_for_errors_async(func: Callable) -> Callable:

    @wraps(func)
    async def wrapper(*args, **kwargs) -> dict:

        response = await func(*args, **kwargs)

        if 'error' in response:

            raise SearchAPIError(response['error'])

        return response

    return wrapper
