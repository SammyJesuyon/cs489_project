from pydantic import BaseModel

class AddressCreateDTO(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class AddressDTO(AddressCreateDTO):
    id: int

    class Config:
        from_attributes = True