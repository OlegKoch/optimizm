from fastapi import HTTPException
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, status, UploadFile, File
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_admin
from src.database import get_db
from src.employees.models import Employee
from src.employees.schemas import EmployeeCreate, EmployeeOut

router = APIRouter(prefix='/api/v1/employees', tags=['employees'])

ALLOWED = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}
MAX_SIZE = 10 * 1024 * 1024
UPLOAD_ROOT = Path("uploads")
BASE_URL_PREFIX = "/static"


@router.post("/", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
async def create_employee(
    payload: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
    admin = Depends(get_current_admin),
):
    emp = Employee(full_name=payload.full_name, position=payload.position)
    db.add(emp)
    await db.commit()
    await db.refresh(emp)
    return emp




@router.post("/{employee_id}/photo", status_code=status.HTTP_201_CREATED)
async def upload_employee_photo(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    file: UploadFile = File(...),
    admin = Depends(get_current_admin),
):
    res = await db.execute(select(Employee).where(Employee.id == employee_id))
    emp = res.scalar_one_or_none()
    if not emp:
        raise HTTPException(404, "Employee not found")

    if file.content_type not in ALLOWED:
        raise HTTPException(415, "Invalid file format. Supported types: JPEG, PNG, WebP")
    ext = ALLOWED[file.content_type]

    folder = UPLOAD_ROOT / "employees" / str(employee_id)
    folder.mkdir(parents=True, exist_ok=False)
    filename = f"{uuid4()}.{ext}"
    disk_path = folder / filename
    rel_path = f"employees/{employee_id}/{filename}"

    size = 0
    with disk_path.open("wb") as dst:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break

            size += len(chunk)
            if size > MAX_SIZE:
                try:
                    disk_path.unlink(missing_ok = True)
                except:
                    pass
                raise HTTPException(413, "File is too large (max 10 MB allowed)")

            dst.write(chunk)

    emp.photo_path = rel_path

    await db.commit()
    return {"photo_url": f"{BASE_URL_PREFIX}/{rel_path}"}




