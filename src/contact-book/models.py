# It defines how a contact look like in python.
from pydantic import (
    BaseModel,
    EmailStr,
)

class Contact(BaseModel):
    name: str
    phone: str
    email: EmailStr | None
    address: str | None
    notes: str | None
    created_at: str
    updated_at: str