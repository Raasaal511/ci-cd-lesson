from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    AlreadyExistsError,
    DomainError,
    DomainValidationError,
    NotFoundError,
)

_STATUS_BY_ERROR: dict[type[DomainError], int] = {
    NotFoundError: status.HTTP_404_NOT_FOUND,
    AlreadyExistsError: status.HTTP_409_CONFLICT,
    DomainValidationError: 422,
}


async def _domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
    status_code = next(
        (code for error, code in _STATUS_BY_ERROR.items() if isinstance(exc, error)),
        status.HTTP_400_BAD_REQUEST,
    )
    return JSONResponse(status_code=status_code, content={"detail": str(exc)})


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, _domain_error_handler)
