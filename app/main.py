from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.routes import routes_health, routes_upload
from app.schemas.schema_base import (
    BaseResponse,
    BaseHttpResponse,
    BaseHttpPaginatedResponse,
)
from app.utils.contants import swagger_description
app = FastAPI(
    title="Retrieval-Augmented Generation",
    description=swagger_description,
    version="1.0.0",
)


# include routers
app.include_router(routes_health.router, tags=["Health"])
app.include_router(routes_upload.router, tags=["Upload"])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=swagger_description,
        routes=app.routes,
    )

    openapi_schema["components"]["schemas"].update({
        "BaseResponse": BaseResponse.schema(),
        "BaseHttpResponse": BaseHttpResponse.schema(),
        "BaseHttpPaginatedResponse": BaseHttpPaginatedResponse.schema(),
    })

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
