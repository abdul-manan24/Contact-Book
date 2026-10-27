# Vallidates input.
from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,

)


class ContactModel(BaseModel):
    id: int | None
    name: str | None
    phone: str
    email: EmailStr
    address: str | None
    notes: str | None
    created_at: str
    updated_at: str

    @field_validator("name")
    @classmethod
    def validate_name():
        pass


    @field_validator("phone")
    @classmethod
    def validate_phone():
        pass
    
    @field_validator("email")
    @classmethod
    def validate_email():
        pass
    
    @field_validator("address")
    @classmethod
    def validate_address():
        pass

    @field_validator("notes")
    @classmethod
    def validate_notes():
        pass
    