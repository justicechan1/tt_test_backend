from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.maps import (
    RouteOutput, PlaceInfo, PathInfo,
    HashtagOutput, TagInfo,
    MoveOutput, MoveInfo
)
from app.models.jeju_cafe import jeju_Cafe
from app.models.jeju_restaurant import jeju_restaurant
from app.models.jeju_tourism import jeju_tourism

router = APIRouter(prefix="/api/users/maps", tags=["maps"])

PLACE_MODELS = [
    jeju_Cafe,
    jeju_restaurant,
    jeju_tourism
]

#@router.get("/route", response_model=RouteOutput)


#@router.get("/hashtag", response_model=HashtagOutput)


#@router.get("/move", response_model=MoveOutput)

