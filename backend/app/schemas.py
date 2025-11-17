from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    class Config:
        orm_mode = True

class TrackCreate(BaseModel):
    title: str
    artist: Optional[str] = None

class TrackOut(BaseModel):
    id: int
    title: str
    artist: Optional[str]
    filename: str
    uploaded_by: Optional[int]
    class Config:
        orm_mode = True
