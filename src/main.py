import os

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.auth.router import router as auth_router
from src.employees.router import router as employees_router
import src.config as config


app = FastAPI(
    title=config.APP_NAME,
    swagger_ui_parameters={"persistAuthorization": True}
)

os.makedirs("uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="uploads"), name="static")

app.include_router(auth_router)
app.include_router(employees_router)




@app.get("/config-check")
async def config_check():
    return {
        'app': config.APP_NAME,
        'db_url': config.DATABASE_URL,
        'jwt': config.JWT_SECRET
    }



