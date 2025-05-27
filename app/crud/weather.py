from sqlalchemy.orm import Session
from app.models.city_search import CitySearch
from sqlalchemy import func

def create_search(db: Session, city: str, user_id: int):
    db_obj = CitySearch(city_name=city, user_id=user_id)
    db.add(db_obj)
    db.commit()


def get_city_stats(db: Session):
    result = db.query(CitySearch.city_name, func.count().label("count"))\
               .group_by(CitySearch.city_name).all()
    # result: List[Tuple[str, int]] → нужно преобразовать:
    return [{"city": city, "count": count} for city, count in result]

