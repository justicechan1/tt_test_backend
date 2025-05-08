from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.jeju_cafe import jeju_Cafe, JejuCafeHashtag
from app.models.jeju_restaurant import jeju_restaurant, JejuRestaurantHashtag
from app.models.jeju_tourism import jeju_tourism, JejuTourismHashtag
from app.schemas.maps import (
    HashtagInput, HashtagOutput, TagInfo,
    MoveOutput,MoveInput,MoveInfo
)

router = APIRouter(prefix="/api/users/maps", tags=["maps"])

PLACE_MODELS = {
    "cafe": (jeju_Cafe, JejuCafeHashtag),
    "restaurant": (jeju_restaurant, JejuRestaurantHashtag),
    "tourism": (jeju_tourism, JejuTourismHashtag)
}

@router.post("/hashtage", response_model=HashtagOutput)
def get_hashtags(input_data: HashtagInput, db: Session = Depends(get_db)):
    category = input_data.category.lower()
    viewport = input_data.viewport

    if category not in PLACE_MODELS:
        raise HTTPException(status_code=400, detail="Invalid category. Choose from cafe, restaurant, tourism")

    PlaceModel, HashtagModel = PLACE_MODELS[category]

    # 1. 뷰포트 범위 내 장소 이름 추출
    subquery = db.query(PlaceModel.name).filter(
        PlaceModel.x_cord >= viewport.min_x,
        PlaceModel.x_cord <= viewport.max_x,
        PlaceModel.y_cord >= viewport.min_y,
        PlaceModel.y_cord <= viewport.max_y
    ).subquery()

    # 2. 해당 장소 이름에 대한 해시태그 추출
    hashtags = db.query(HashtagModel.hashtag_name).filter(
        HashtagModel.name.in_(subquery)
    ).distinct().all()

    return HashtagOutput(tag=[TagInfo(hashtag_name=row.hashtag_name) for row in hashtags])

@router.post("/move", response_model=MoveOutput)
def get_move_candidates(input_data: MoveInput, db: Session = Depends(get_db)):
    tags = [t.hashtag_name for t in input_data.tag]
    viewport = input_data.viewport
    results = []

    for category, (PlaceModel, HashtagModel) in PLACE_MODELS.items():
        # 1. 뷰포트 범위 내 장소 이름 추출
        subquery = db.query(PlaceModel.name).filter(
            PlaceModel.x_cord >= viewport.min_x,
            PlaceModel.x_cord <= viewport.max_x,
            PlaceModel.y_cord >= viewport.min_y,
            PlaceModel.y_cord <= viewport.max_y
        ).subquery()

        # 2. 해당 이름 중, 해시태그가 포함되는 것만 필터링
        tagged_names = db.query(HashtagModel.name).filter(
            HashtagModel.name.in_(subquery),
            HashtagModel.hashtag_name.in_(tags)
        ).distinct().all()

        name_list = [r.name for r in tagged_names]

        if not name_list:
            continue

        # 3. 실제 장소 정보 추출
        places = db.query(PlaceModel.name, PlaceModel.x_cord, PlaceModel.y_cord).filter(
            PlaceModel.name.in_(name_list)
        ).all()

        for p in places:
            results.append(MoveInfo(name=p.name, x_cord=float(p.x_cord), y_cord=float(p.y_cord)))

    return MoveOutput(move=results)

