from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud import weather
from app.models.city_search import CitySearch
from app.services.weather_service import fetch_weather
from typing import List
from app.schemas.weather import CityStat
from app.services.autocomplete_service import autocomplete_city
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/weather")
async def get_weather(city: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    weather.create_search(db, city, user.id)
    data = await fetch_weather(city)
    return {"city": city, "forecast": data}


@router.get("/stats", response_model=List[CityStat])
def get_stats(db: Session = Depends(get_db)):
    return weather.get_city_stats(db)


@router.get("/autocomplete")
async def get_city_suggestions(q: str):
    return await autocomplete_city(q)

@router.get("/history")
def user_search_history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    history = db.query(CitySearch.city_name, CitySearch.searched_at)\
        .filter(CitySearch.user_id == user.id)\
        .order_by(CitySearch.searched_at.desc()).all()
    return [{"city": c, "time": str(t)} for c, t in history]
