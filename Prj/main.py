from fastapi import FastAPI
import uvicorn
from core.database import SessionLocal
from sqlalchemy.orm import Session
from core.models import Farmer
app = FastAPI()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}


def create_farmer(db: Session, farmer_data: dict):
    db_farmer = Farmer(**farmer_data)
    db.add(db_farmer)
    db.commit()
    db.refresh(db_farmer)
    return db_farmer

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)