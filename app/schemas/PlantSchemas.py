from typing import Dict, List
from pydantic import BaseModel


class PlantAttribute(BaseModel):
    name: str
    info1: str
    info2: str


class PlantingCondition(BaseModel):
    condition: str
    min: int
    max: int


class PlantDetails(BaseModel):
    name: str
    description: str
    scientific_name: str
    planting_conditions: List[PlantingCondition]
    info: List[PlantAttribute]
    image_urls: List[str]


class SearchPlantResult(BaseModel):
    id: str
    name: str
    thumbnail_url: str


class SearchPlantList(BaseModel):
    results: List[SearchPlantResult]
