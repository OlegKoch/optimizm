from pydantic import BaseModel, Field

class EmployeeCreate(BaseModel):
    full_name: str = Field(min_length=3, max_length=128)
    position: str = Field(min_length=2, max_length=64)

class EmployeeOut(BaseModel):
    id: int
    full_name: str
    position: str
    photo_url: str | None = None

    class Config:
        from_attributes = True