# routers/db_checker.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.jeju_cafe import jeju_Cafe
from app.models.jeju_restaurant import jeju_restaurant
from app.models.jeju_tourism import jeju_tourism

router = APIRouter(prefix="/api/db", tags=["DB Checker"])

PLACE_MODELS = {
    "cafe": jeju_Cafe,
    "restaurant": jeju_restaurant,
    "tourism": jeju_tourism
}

@router.get("/check_place")
def check_place(name: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    for category, Model in PLACE_MODELS.items():
        db_place = db.query(Model).filter(Model.name == name).first()
        if db_place:
            return {"status": "exists", "category": category}
    
    return {"status": "not_found"}
