from fastapi import FastAPI
from app.db.session import close_db_connection

app = FastAPI()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db_connection()