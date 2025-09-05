from fastapi import APIRouter
from app.schemas.schema_base import BaseResponse
from app.services.service_health import check_health


router = APIRouter()


@router.get("/health", response_model=BaseResponse)
async def health_check():
    return await check_health()
