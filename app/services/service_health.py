from app.schemas.schema_base import BaseResponse
from fastapi import status


async def check_health() -> BaseResponse:
    return BaseResponse(
        status=status.HTTP_200_OK,
        message="Service is healthy"
    )
