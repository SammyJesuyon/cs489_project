from fastapi import HTTPException, status
from fastapi import Request
from fastapi.responses import JSONResponse

class NotFoundException(HTTPException):
    def __init__(self, entity: str, entity_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity} with id {entity_id} not found",
        )

class ConflictException(HTTPException):
    def __init__(self, message: str = "Conflict: entity already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message,
        )

class BadRequestException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if exc.detail else "HTTP error occurred",
            "code": exc.status_code,
            "details": str(exc)
        },
    )

def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "code": 500,
            "details": str(exc)
        },
    )
