from fastapi import FastAPI
from app.routers import docs


app = FastAPI()


app.include_router(docs.router)
@app.get("/")
async def root():
    return {"message": "Ok"}
