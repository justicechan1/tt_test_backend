from pydantic import BaseModel
from typing import List, Optional, Dict


# ------------------- /api/places/edit -------------------
class PlaceNameOnly(BaseModel):
    name: str

class PlaceEditInput(BaseModel):
    places_by_day: Dict[str, List[PlaceNameOnly]]

class PlaceEditOutput(BaseModel):
    places_by_day: Dict[str, List[PlaceNameOnly]]


# ------------------- /api/places/search -------------------
class PlaceSearchResult(BaseModel):
    name: str

class PlaceSearchOutput(BaseModel):
    search: List[PlaceSearchResult]


# ------------------- /api/places/data -------------------
class PlaceDataResult(BaseModel):
    name: str
    address: str
    phone: Optional[str] = None
    convenience: Optional[str] = None
    category: Optional[str] = None
    website: Optional[str] = None
    business_hours: Optional[str] = None
    open_time: Optional[str] = None
    close_time: Optional[str] = None
    image_urls: List[str]

    class Config:
        orm_mode = True

class PlaceDataResponse(BaseModel):
    places: PlaceDataResult