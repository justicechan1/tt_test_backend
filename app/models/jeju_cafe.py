#models\main_cafe.py
from sqlalchemy import Column, Integer, String, Float, Text, DECIMAL
from app.database import Base

class jeju_Cafe(Base):
    __tablename__ = "jeju_cafe"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    category = Column(String(255))
    page_url = Column(Text)
    score = Column(Float)
    address = Column(Text)
    phone = Column(String(100))
    convenience = Column(Text)
    website = Column(Text)
    y_cord = Column(DECIMAL(10, 7))
    x_cord = Column(DECIMAL(10, 7))
    open_time = Column(String(255))
    close_time = Column(String(255))
    break_time = Column(String(255))
    service_time = Column(String(255))
    closed_days = Column(String(255))

    class Config:
        orm_mode = True

class JejuCafeImage(Base):
    __tablename__ = "jeju_cafe_image"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    url_1 = Column(String(500))
    url_2 = Column(String(500))
    url_3 = Column(String(500))
    url_4 = Column(String(500))
    url_5 = Column(String(500))
    url_6 = Column(String(500))

    class Config:
        orm_mode = True

class JejuCafeHashtag(Base):
    __tablename__ = "jeju_cafe_hashtags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    place_name = Column(String, index=True)
    hashtag_name = Column(String)

    class Config:
        orm_mode = True