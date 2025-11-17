from sqlalchemy.orm import Session
from . import models, schemas, auth
from fastapi import HTTPException
import os, shutil

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def create_user(db: Session, user: schemas.UserCreate):
    hashed = auth.hash_password(user.password)
    db_user = models.User(email=user.email, username=user.username, password_hash=hashed)
    db.add(db_user)
    try:
        db.commit(); db.refresh(db_user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email or username already used")
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter((models.User.username==username) | (models.User.email==username)).first()
    if not user: return None
    if not auth.verify_password(password, user.password_hash): return None
    return user

def save_track_file(file_obj, filename):
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file_obj, f)
    return path

def create_track(db: Session, track_data: schemas.TrackCreate, filename: str, user_id: int):
    t = models.Track(title=track_data.title, artist=track_data.artist, filename=filename, uploaded_by=user_id)
    db.add(t)
    db.commit(); db.refresh(t)
    return t

def list_tracks(db: Session, skip=0, limit=50):
    return db.query(models.Track).order_by(models.Track.created_at.desc()).offset(skip).limit(limit).all()

def get_track(db: Session, track_id: int):
    return db.query(models.Track).filter(models.Track.id==track_id).first()
