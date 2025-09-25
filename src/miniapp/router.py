from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from src.services.models import Service
from src.employees.models import Employee
from src.miniapp.models import MiniAppsApplications
from src.database import get_db
from src.miniapp.schemas import MiniappOrderCreate, MiniappOrderOut
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/api/v1/miniapp-orders', tags=['miniapp-orders'])


class MiniappOrder:
    pass


@router.post('/', response_model=MiniappOrderOut, status_code=status.HTTP_201_CREATED)
async def create_miniapp_order(
        payload: MiniappOrderCreate,
        db: AsyncSession = Depends(get_db)
):
    svc = await db.scalar(select(Service.id).where(Service.id == payload.service_id))
    if not svc:
        raise HTTPException(status_code=404, detail='Service not found')

    emp = await db.scalar(select(Employee.id).where(Employee.id == payload.employee_id))
    if not emp:
        raise HTTPException(status_code=404, detail='Employee not found')

    order = MiniAppsApplications(
        service_id=payload.service_id,
        employee_id=payload.employee_id,
        client_name=payload.client_name,
        client_phone=payload.client_phone,
        tg_id=payload.tg_id,
        tg_username=payload.tg_username,
        comment=payload.comment
    )

    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order
