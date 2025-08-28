import logging

from fastapi import Request, status
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from main import main_app


log = logging.getLogger(__name__)


@main_app.exception_handlers(ValidationError)
def handle_pydantic_validation_error(
        request: Request,
        exc: ValidationError,
) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Unhandled error",
            "error": exc.errors()
        }
    )


@main_app.exception_handlers(SQLAlchemyError)
def handle_sqlalchemy_error(
        request: Request,
        exc: ValidationError,
) -> ORJSONResponse:
    log.error("Unhandled SQLAlchemy error", exc_info=exc)
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "An unexpected error has occurred. Our admins are already working on it."
        }
    )