from fastapi import FastAPI

from .api import router

app = FastAPI(title="Items catalogue", description="FastAPI + OOP layered architecture (AIDAMS OOP course)")
app.include_router(router)
