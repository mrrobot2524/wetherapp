import httpx

async def autocomplete_city(query: str, limit: int = 5):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": query,
                "format": "json",
                "limit": limit,
                "addressdetails": 1
            },
            headers={"User-Agent": "WeatherApp"}
        )
        data = response.json()
        results = []
        for item in data:
            if item.get("type") == "city" or "city" in item.get("display_name", "").lower():
                results.append({
                    "name": item.get("display_name"),
                    "lat": item.get("lat"),
                    "lon": item.get("lon")
                })
        return results
