from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Dict
from sqlalchemy import func
from app.database import get_db
from app.models.jeju_cafe import jeju_Cafe, JejuCafeImage
from app.models.jeju_restaurant import jeju_restaurant, JejuRestaurantImage
from app.models.jeju_tourism import jeju_tourism, JejuTourismImage
from app.cache import user_schedules
from app.schemas.places import (
    PlaceSearchOutput, PlaceSearchResult,
    PlaceDataResponse, PlaceDataResult,
    PlaceEditInput, PlaceEditOutput, PlaceNameOnly
)

router = APIRouter(prefix="/api/places", tags=["places"])

PLACE_MODELS = {
    "cafe": (jeju_Cafe, JejuCafeImage),
    "restaurant": (jeju_restaurant, JejuRestaurantImage),
    "tourism": (jeju_tourism, JejuTourismImage)
}

def fetch_image_urls(db: Session, image_model, name: str) -> list[str]:
    db_image = db.query(image_model).filter(
        func.trim(func.lower(image_model.name)) == func.trim(func.lower(name))
    ).first()
    if not db_image:
        return []
    return [
        getattr(db_image, f"url_{i}") for i in range(1, 7)
        if getattr(db_image, f"url_{i}")
    ]

@router.get("/search", response_model=PlaceSearchOutput)
def search_places(name: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    search_term = f"%{name.strip()}%"
    results = []
    for model_type, (model, _) in PLACE_MODELS.items():
        try:
            matches = db.query(model).filter(model.name.like(search_term)).all()
            for match in matches:
                results.append(PlaceSearchResult(name=match.name, type=model_type))
        except Exception as e:
            print(f"[{model_type}] 검색 중 오류 발생: {str(e)}")
    return PlaceSearchOutput(search=results)

@router.get("/data", response_model=PlaceDataResponse)
def get_place_detail(name: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    place_name = name.strip()
    for _, (place_model, image_model) in PLACE_MODELS.items():
        place = db.query(place_model).filter(place_model.name == place_name).first()
        if place:
            image_urls = fetch_image_urls(db, image_model, place_name)
            return PlaceDataResponse(
                places=PlaceDataResult(
                    name=place.name,
                    address=place.address,
                    phone=getattr(place, "phone", None),
                    convenience=getattr(place, "convenience", None),
                    category=getattr(place, "category", None),
                    website=getattr(place, "website", None),
                    business_hours=getattr(place, "business_hours", None),
                    open_time=getattr(place, "open_time", None),
                    close_time=getattr(place, "close_time", None),
                    image_urls=image_urls
                )
            )
    raise HTTPException(status_code=404, detail="해당 장소는 데이터베이스에 존재하지 않습니다.")

@router.post("/add", response_model=PlaceEditOutput)
def add_place(input_data: PlaceEditInput, user_id: str = Query(...), db: Session = Depends(get_db)):
    if user_id not in user_schedules:
        raise HTTPException(status_code=404, detail="해당 사용자의 일정이 존재하지 않습니다.")

    user_data = user_schedules[user_id]

    for date, places in input_data.places_by_day.items():
        if date not in user_data["places_by_day"]:
            user_data["places_by_day"][date] = []

        existing_names = [p["name"] for p in user_data["places_by_day"][date]]

        for place in places:
            place_name = place.name.strip()
            if place_name in existing_names:
                continue

            db_match = None
            model_type = None
            for _type, (model, _) in PLACE_MODELS.items():
                db_match = db.query(model).filter(model.name == place_name).first()
                if db_match:
                    model_type = _type
                    break

            if not db_match:
                raise HTTPException(status_code=404, detail=f"{place_name} 은 데이터베이스에 존재하지 않습니다.")

            image_urls = fetch_image_urls(db, PLACE_MODELS[model_type][1], place_name)

            user_data["places_by_day"][date].append({
                "name": db_match.name,
                "address": db_match.address,
                "phone": getattr(db_match, "phone", None),
                "convenience": getattr(db_match, "convenience", None),
                "category": model_type,
                "website": getattr(db_match, "website", None),
                "business_hours": getattr(db_match, "business_hours", None),
                "open_time": getattr(db_match, "open_time", None),
                "close_time": getattr(db_match, "close_time", None),
                "image_urls": image_urls
            })

    return PlaceEditOutput(places_by_day=user_data["places_by_day"])

@router.post("/remove", response_model=PlaceEditOutput)
def remove_place(input_data: PlaceEditInput, user_id: str = Query(...)):
    if user_id not in user_schedules:
        raise HTTPException(status_code=404, detail="해당 사용자의 일정이 존재하지 않습니다.")

    user_data = user_schedules[user_id]

    for date, places in input_data.places_by_day.items():
        if date not in user_data["places_by_day"]:
            continue

        for place in places:
            place_name = place.name.strip()
            user_data["places_by_day"][date] = [
                p for p in user_data["places_by_day"][date] if p["name"] != place_name
            ]

    return PlaceEditOutput(places_by_day=user_data["places_by_day"])