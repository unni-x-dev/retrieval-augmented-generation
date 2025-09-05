from pydantic import BaseModel


class BaseResponse(BaseModel):
    """Minimal response schema containing a status and a message.

    Attributes:
        status (str): Indicates whether the request was successful
        (e.g., "ok", "error").
        message (str): A human-readable description or additional information
        about the response.
    """
    status: int
    message: str


class BaseHttpResponse(BaseResponse):
    """Standard HTTP response schema with a data payload.

    Extends BaseResponse by adding:
        data (dict): The main response content, typically a single resource
            or a structured object returned by the API.
    """
    data: dict


class BaseHttpPaginatedResponse(BaseHttpResponse):
    """HTTP response schema for paginated results.

    Extends BaseHttpResponse by adding:
        pagination (dict): Metadata about the paginated result set, such as
            page number, page size, and total number of items.
    """
    pagination: dict
