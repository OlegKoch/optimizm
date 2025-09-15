from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from src.auth.schemas import UserOut, RegisterIn, TokenOut, LoginIn
from src.database import get_db
from src.auth.utils import hash_password, verify_password, create_jwt_token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.auth.models import User

router = APIRouter(prefix="/auth", tags= ["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterIn, db: AsyncSession = Depends(get_db)):
    user = User(
        username=payload.username,
        pass_hash=hash_password(payload.password),
        role="user"
    )
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Username already taken")

    await db.refresh(user)
    return user




@router.post("/login", response_model=TokenOut)
async def login(payload: LoginIn, db: AsyncSession = Depends(get_db)):
    try:
        res = await db.execute(select(User).where(User.username == payload.username))
        user = res.scalar_one_or_none()

        if not user:
            raise ValueError("User not found")

        if not verify_password(payload.password, user.pass_hash):
            raise ValueError("Invalid password")

        token = create_jwt_token(sub=user.username)
        return {"access_token": token, "token_type": "bearer"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
