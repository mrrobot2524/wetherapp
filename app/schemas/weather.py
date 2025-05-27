from pydantic import BaseModel

class CityStat(BaseModel):
    city: str
    count: int
