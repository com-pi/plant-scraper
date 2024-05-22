from typing import Dict, List
from pydantic import BaseModel


class PlantAttribute(BaseModel):
    name: str
    info1: str
    info2: str

class PlantDetails(BaseModel):
    name: str
    description: str
    scientific_name: str
    info: List[PlantAttribute]

class SearchPlantResult(BaseModel):
    name: str
    thumbnail_url: str

class SearchPlantList(BaseModel):
    results: List[SearchPlantResult]

