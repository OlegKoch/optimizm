from pydantic import BaseModel, Field, condecimal


class ServiceCreate(BaseModel):
    name: str =  Field(min_length=2, max_length=128)
    price: condecimal(max_digits=10, decimal_places=2)
    description: str | None
    is_active: bool = True



class ServiceOut(BaseModel):
    id: int
    name: str
    price: condecimal(max_digits=10, decimal_places=2)
    description: str | None
    is_active: bool = True

    class Config:
        from_attributes = True
