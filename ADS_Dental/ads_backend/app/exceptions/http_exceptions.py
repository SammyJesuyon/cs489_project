from fastapi import HTTPException, status

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