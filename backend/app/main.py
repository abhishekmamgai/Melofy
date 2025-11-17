# backend/app/main.py

from fastapi import (
    FastAPI,
    Depends,
    UploadFile,
    File,
    HTTPException,
    status,
    Header,
    Query
)
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database, crud, auth
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Jamendo API Client ID
JAMENDO_CLIENT_ID = os.getenv("JAMENDO_CLIENT_ID")

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

# FastAPI app
app = FastAPI(title="Melofy API")

# CORS (allow frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static folder (for uploaded songs)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ---------- DB Dependency ----------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- HOME ROUTE ----------
@app.get("/")
def home():
    return {"message": "Melofy backend is running 🎵", "docs": "/docs"}


# ---------- AUTH ROUTES ----------
@app.post("/api/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.post("/api/login")
def login(payload: dict, db: Session = Depends(get_db)):
    username = payload.get("username")
    password = payload.get("password")

    user = crud.authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = auth.create_access_token({"sub": user.username, "user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "username": user.username},
    }


# ---------- TRACK UPLOAD ----------
@app.post("/api/tracks/upload", response_model=schemas.TrackOut)
def upload_track(
    title: str,
    artist: str | None = None,
    file: UploadFile = File(...),
    authorization: str = Header(None),
    db: Session = Depends(get_db),
):
    # Token check
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization")

    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = authorization.split(" ", 1)[1]
    payload = auth.decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("user_id")

    # Safe file name
    import time
    safe_name = file.filename.replace(" ", "_")
    filename = f"{user_id}_{int(time.time())}_{safe_name}"

    # Save file
    crud.save_track_file(file.file, filename)

    # Create DB entry
    track = crud.create_track(
        db,
        schemas.TrackCreate(title=title, artist=artist),
        filename,
        user_id,
    )
    return track


# ---------- GET TRACKS ----------
@app.get("/api/tracks")
def tracks(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    ts = crud.list_tracks(db, skip, limit)
    return [
        {
            "id": t.id,
            "title": t.title,
            "artist": t.artist,
            "filename": t.filename,
        }
        for t in ts
    ]


# ---------- JAMENDO SEARCH ----------
@app.get("/api/search")
def search_jamendo(q: str = Query(..., min_length=1)):
    """
    Search royalty-free songs from Jamendo API.
    """
    if not JAMENDO_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Jamendo client ID missing.")

    url = "https://api.jamendo.com/v3.0/tracks"
    params = {
        "client_id": JAMENDO_CLIENT_ID,
        "format": "json",
        "limit": 20,
        "namesearch": q,
        "audioformat": "mp32",
    }

    try:
        res = requests.get(url, params=params, timeout=10)
    except Exception:
        raise HTTPException(status_code=502, detail="Could not reach Jamendo API")

    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail="Jamendo API error")

    data = res.json()
    results = []

    for t in data.get("results", []):
        results.append({
            "id": t.get("id"),
            "title": t.get("name"),
            "artist": t.get("artist_name"),
            "image": t.get("image"),
            "audio_url": t.get("audio"),
            "jamendo_url": t.get("shareurl"),
        })

    return {"results": results}
