from pydantic import BaseModel

class AnalysisInput(BaseModel):
    latitude: float
    longitude: float
    categories: list[str]
    search_area: dict

class Competitor(BaseModel):
    name: str
    category: str
    subcategory: str
    address: str
    latitude: float
    longitude: float
    distance_meters: float

class AnalysisResult(BaseModel):
    target_location: dict          # {"latitude": ..., "longitude": ...}
    competitors: list[Competitor]
    total_competitors: int
    average_distance_meters: float | None
    nearest_competitor_distance: float | None
    competition_density: str       # "LOW", "MEDIUM" oppure "HIGH"