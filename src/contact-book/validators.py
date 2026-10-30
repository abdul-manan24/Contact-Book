# Vallidates input.
from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    Field
)


class ContactModel(BaseModel):
    
    id: int | None = None
    name: str | None = Field(min_length=3, max_length=50)
    phone: str | None = Field(min_length=10, max_length=15)
    email: EmailStr | None
    address: str | None = Field(min_length=5, max_length=100)
    notes: str | None = Field(min_length=5, max_length=100)

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:

        if name is None:
            return name
        
        is_valid = bool(name and all(char.isalpha() or char.isspace() for char in name))
        if not is_valid:
            raise ValueError("Name must only contain letters and spaces.")
        return name

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone: str) -> str:

        if phone is None:
            return phone

        phone = phone.strip()
           
        is_valid = bool(phone and all(char.isnumeric() or char in ('-',' ', '+') for char in phone))

        if not is_valid:
            raise ValueError("Phone must only contain numbers.")
        
        return phone