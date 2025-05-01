# from pydantic import BaseModel
# from typing import List, Dict, Optional

# # ------------------- 공통 -------------------

# class TagInfo(BaseModel):
#     hashtag_name: str

# class MoveInfo(BaseModel):
#     name: str
#     x_cord: float
#     y_cord: float

# class PathInfo(BaseModel):
#     # 실제 경로 정보가 확정되면 구조 정의
#     pass

# # ------------------- 경로 최적화 -------------------

# class RoutePlaceInput(BaseModel):
#     name: str

# class RouteInput(BaseModel):
#     user_id: str
#     places_by_day: Dict[str, List[RoutePlaceInput]]

# class PlaceInfo(BaseModel):
#     id: int
#     name: str
#     x_cord: float
#     y_cord: float
#     category: str
#     open_time: str
#     close_time: str
#     service_time: int
#     tags: List[str]
#     closed_days: List[str]
#     break_time: List[str]
#     is_mandatory: bool

# class RouteOutput(BaseModel):
#     places_by_day: Dict[str, List[PlaceInfo]]
#     path: List[PathInfo]

# # ------------------- 해시태그 -------------------

# class HashtagInput(BaseModel):
#     category: str
#     user_x_cord: float
#     user_y_cord: float

# class HashtagOutput(BaseModel):
#     tag: List[TagInfo]

# # ------------------- 지도 새로고침 -------------------

# class MoveInput(BaseModel):
#     tag: List[TagInfo]
#     user_x_cord: float
#     user_y_cord: float

# class MoveOutput(BaseModel):
#     move: List[MoveInfo]
