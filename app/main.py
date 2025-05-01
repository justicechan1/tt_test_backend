#main.py
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import places
from app.routers import schedule_chche
from app.routers import maps
from app.routers import db_checker

# 테이블 생성 (자동)
Base.metadata.create_all(bind=engine)

app = FastAPI()


# 라우터 등록
app.include_router(schedule_chche.router)
app.include_router(places.router)
app.include_router(maps.router)
app.include_router(db_checker.router)

@app.get("/")
def root():
    return {"message": "MainCafe API"}
