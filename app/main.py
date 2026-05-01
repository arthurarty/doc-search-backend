from fastapi import FastAPI

from app.routers import docs
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI()
origins = settings.cors_origins.split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(docs.router)


@app.get("/")
async def root():
    return {"message": "Ok"}
