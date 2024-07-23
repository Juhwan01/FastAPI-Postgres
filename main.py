from fastapi import Depends, FastAPI
import uvicorn
from core import base

app=FastAPI()

base.Base.metadata.create_all(base.engine)

def get_db():
    db = base.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/api/")
def root():
    return {"message" : "Hello World"}

@app.get("/api/users")
def get_users(skip: int = 0, limit: int = 100, db = Depends(get_db)):
    return db.query(base.User).offset(skip).limit(limit).all()

@app.get("/api/createuser")
def create_user(username: str, email: str, password: str, db = Depends(get_db)):
    db_user = base.User(username=username, email=email, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

