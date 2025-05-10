#schemas\schedule.py
from pydantic import BaseModel
from typing import List, Dict, Optional, Union

# ------------------- /init 요청 -------------------

class DateInfo(BaseModel):
    user_id: str
    start_date: str
    end_date: str

class StartEndInfo(BaseModel):
    arrival: str
    arrivaltime: str
    departure: str
    departuretime: str

class MealTimePreferences(BaseModel):
    breakfast: List[str]
    lunch: List[str]
    dinner: List[str]

class UserPreference(BaseModel):
    start_time: str
    end_time: str
    travel_style: str
    meal_time_preferences: MealTimePreferences

class PlaceSimpleInput(BaseModel):
    name: str

class ScheduleInitInput(BaseModel):
    date: DateInfo
    start_end: StartEndInfo
    user: UserPreference
    places_by_day: Dict[str, List[PlaceSimpleInput]]


# ------------------- /init 응답 -------------------

class PlaceDetailOutput(BaseModel):
    id: int
    name: str
    x_cord: float
    y_cord: float
    category: str
    open_time: Optional[str] = ""
    close_time: Optional[str] = ""
    service_time: Optional[int] = 0
    tags: List[str] = []
    closed_days: List[str] = []
    break_time: List[str] = []
    is_mandatory: Optional[bool] = False

class ScheduleInitOutput(BaseModel):
    date: DateInfo
    start_end: StartEndInfo
    places_by_day: Dict[str, List[PlaceDetailOutput]]


# ------------------- /init_show 요청 -------------------

class ScheduleShowInput(BaseModel):
    user_id: str


# ------------------- /init_show 응답 -------------------

class PlaceInfoOutputByDay(BaseModel):
    name: str
    address: str
    phone: Optional[str] = ""
    convenience: Optional[str] = ""
    category: Optional[str] = ""
    website: Optional[str] = ""
    business_hours: Optional[str] = ""
    open_time: Optional[str] = ""
    close_time: Optional[str] = ""
    image_urls: Optional[List[str]] = []

class ScheduleShowOutput(BaseModel):
    date: DateInfo
    start_end: StartEndInfo
    places_by_day: Dict[str, List[PlaceInfoOutputByDay]]