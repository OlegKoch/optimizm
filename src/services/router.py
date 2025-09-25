from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.database import get_db
from src.services.models import Service
from src.services.schemas import ServiceOut, ServiceCreate
from src.auth.dependencies import get_current_admin
from fastapi import APIRouter, status, Depends, HTTPException

router = APIRouter(prefix='/api/v1/services', tags=['services'])

@router.post('/', response_model=ServiceOut, status_code=status.HTTP_201_CREATED)
async def create_service(
        payload: ServiceCreate,
        db: AsyncSession = Depends(get_db),
        admin = Depends(get_current_admin),

):
    svc = Service(
        name = payload.name,
        price = payload.price,
        description = payload.description,
        is_active = payload.is_active,
    )
    db.add(svc)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Service with this name already exists')

    await db.refresh(svc)
    return svc


