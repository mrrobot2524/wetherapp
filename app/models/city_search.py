from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from app.core.database import Base


class CitySearch(Base):
    __tablename__ = "city_searches"

    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String, index=True)
    searched_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

