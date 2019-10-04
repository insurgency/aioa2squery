from functools import wraps
from warnings import warn

__all__ = (
    'deprecated',
)


def deprecated(*, message: str):
    """
    Function decorator to emit an unconditional warning message before invocation of wrapped function

    :param message: Message text to emit in warning
    :type message: str
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Emit deprecation warning message before calling wrapped function
            warn(message, DeprecationWarning)
            # Call original function and return...
            return func(*args, **kwargs)
        return wrapper
    return decorator
