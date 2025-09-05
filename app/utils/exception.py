from functools import wraps
from fastapi import HTTPException
from starlette import status


def handle_exceptions(func):
    """
    Decorator to handle exceptions in FastAPI route handlers.

    - Re-raises HTTPException directly (preserves status_code and detail).
    - Wraps unexpected errors into HTTP 500 responses.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as e:
            # Pass through FastAPI's HTTPException
            raise e
        except Exception as e:
            # Catch-all for unexpected errors
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
    return wrapper
