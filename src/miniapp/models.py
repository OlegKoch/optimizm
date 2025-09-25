from datetime import datetime
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Integer, ForeignKey, BigInteger, Text


class MiniAppsApplications(Base):
    __tablename__ = 'miniapp_application'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    service_id: Mapped[int] = mapped_column(ForeignKey('services.id', ondelete='RESTRICT'), nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey('employees.id', ondelete='RESTRICT'), nullable=False)

    client_name: Mapped[str] = mapped_column(String(120), nullable=False)
    client_phone: Mapped[str] = mapped_column(String(32), nullable=False)
    tg_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    tg_username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow(), nullable=False)

    service = relationship('Service', lazy='joined')
    employee = relationship('Employee', lazy='joined')

