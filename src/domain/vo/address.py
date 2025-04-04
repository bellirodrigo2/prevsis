from pydantic import BaseModel


class Address(BaseModel):

    street: str | None
    number: str | None
    neighborhood: str | None
    city: str
    state: str
    zip_code: str | None
