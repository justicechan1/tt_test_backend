#main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ 반드시 FastAPI 생성 이후에 설정
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",  # 개발용: 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 나머지 import 및 라우터 등록
from app.routers import places, schedule_chche, maps, db_checker
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app.include_router(schedule_chche.router)
app.include_router(places.router)
app.include_router(maps.router)
app.include_router(db_checker.router)


@app.get("/")
def root():
    return {"message": "MainCafe API"}