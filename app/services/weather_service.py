import httpx
from app.core.config import settings

async def fetch_weather(city: str):
    # Пример статичных координат, позже добавим автоопределение по названию
    params = {
        "latitude": 50,
        "longitude": 50,
        "hourly": "temperature_2m"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.OPEN_METEO_URL, params=params)
        return response.json()
