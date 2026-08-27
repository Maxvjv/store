from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import *
from app.api.v1 import *



@asynccontextmanager
async def lifespan(app: FastAPI):
# Создание таблиц (временно, позже заменим на миграции)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
app = FastAPI(title="Online Shop API", lifespan=lifespan)
@app.get("/")
async def root():
    return {"message": "Hello W56rtorld"}
@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(router_product)
app.include_router(router_user)
app.include_router(router_category)
app.include_router(router_cart)
app.include_router(router_favorite)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers=['*'],

)

print('Help')