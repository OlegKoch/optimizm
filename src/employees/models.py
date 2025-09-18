from sqlalchemy import Column, Integer, String
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    position: Mapped[str] = mapped_column(String(64), nullable=False)
    photo_path: Mapped[str | None] = mapped_column(String(512), nullable=True)