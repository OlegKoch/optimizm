from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class MiniappOrderCreate(BaseModel):
    service_id: int = Field(gt=0)
    employee_id: int = Field(gt=0)

    client_name: str = Field(max_length=120)
    client_phone: str = Field(None, max_length=32)

    @field_validator("client_phone")
    def check_phone(cls, v):
        if v is None:
            return v
        if not v.startswith("+7"):
            raise ValueError("Телефон должен начинаться с +7")
        if len(v) < 12:
            raise ValueError("Слишком короткий номер телефона")
        return v

    tg_id: int | None = None
    tg_username: str | None = Field(None, max_length=120)
    comment: str | None = None

class MiniappOrderOut(BaseModel):
    id: int
    service_id: int
    employee_id: int
    client_name: str
    client_phone: str
    tg_id: int | None
    tg_username: str | None
    comment: str | None
    created_at: datetime

    class Config:
        from_attributes = True
