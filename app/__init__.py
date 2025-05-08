from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS 설정은 라우터 등록 전에 해야 함
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 테스트용, 운영 시 특정 origin만 허용 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 라우터는 그 다음 등록
from app.routers import maps, places, schedule_chche

app.include_router(maps.router, prefix="/api/users/maps")
app.include_router(places.router, prefix="/api/places")
app.include_router(schedule_chche.router, prefix="/api/users/schedules")
