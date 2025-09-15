from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.router import router as auth_router
from src.employees.router import router as employees_router
import src.config as config
from src.database import get_db

app = FastAPI(
    title=config.APP_NAME,
    swagger_ui_parameters={"persistAuthorization": True}
)

app.include_router(auth_router)
app.include_router(employees_router)




@app.get("/config-check")
async def config_check():
    return {
        'app': config.APP_NAME,
        'db_url': config.DATABASE_URL,
        'jwt': config.JWT_SECRET
    }



