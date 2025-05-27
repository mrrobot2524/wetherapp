from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.auth.dependencies import get_current_user
from app.models.city_search import CitySearch
from app.models.user import User

router = APIRouter()


@router.post("/history")
def add_to_history(
        data: dict = Body(...),
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    city = data.get("city")
    if not city:
        raise HTTPException(status_code=400, detail="City is required")

    new_entry = CitySearch(user_id=user.id, city_name=city)
    db.add(new_entry)
    db.commit()
    return {"message": "Added to history"}


@router.delete("/history")
def clear_user_history(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    db.query(CitySearch).filter(CitySearch.user_id == user.id).delete()
    db.commit()
    return {"message": "History cleared"}


@router.get("/history")
def get_user_history(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    history = (
        db.query(CitySearch.city_name)
        .filter(CitySearch.user_id == user.id)
        .order_by(CitySearch.searched_at.desc())
        .all()
    )
    return [row[0] for row in history]
