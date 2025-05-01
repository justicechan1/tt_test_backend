#schemas\main_restaurant.py
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class jeju_restaurantBase(BaseModel):
    name: str
    category: Optional[str] = None
    page_url: Optional[str] = None
    score: Optional[float] = None
    address: str
    phone: Optional[str] = None
    convenience: Optional[str] = None
    broadcast: Optional[str] = None
    website: Optional[str] = None
    y_cord: Optional[Decimal] = None
    x_cord: Optional[Decimal] = None
    close_time: Optional[Decimal] = None
    open_time: Optional[Decimal] = None
    break_time: Optional[Decimal] = None
    service_time: Optional[Decimal] = None
    closed_days: Optional[Decimal] = None
