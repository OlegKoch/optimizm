from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_admin
from src.database import get_db
from src.employees.models import Employee
from src.employees.schemas import EmployeeCreate, EmployeeOut

router = APIRouter(prefix='/employees', tags=['employees'])

@router.post("/", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
async def create_employee(
        payload: EmployeeCreate,
        db: AsyncSession = Depends(get_db),
        admin=Depends(get_current_admin)
):
    emp = Employee(full_name=payload.full_name, position=payload.position)
    db.add(emp)
    await db.commit()
    await db.refresh(emp)
    return emp
