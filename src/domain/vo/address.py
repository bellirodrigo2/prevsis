from pydantic import BaseModel


class Address(BaseModel):

    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    zip_code: str

    class Config:
        orm_mode = True
