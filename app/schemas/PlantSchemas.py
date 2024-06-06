from typing import List
from pydantic import BaseModel


class PlantAttribute(BaseModel):
    name: str
    info1: str
    info2: str


class PlantingCondition(BaseModel):
    condition: str
    min: int
    max: int

    @classmethod
    def from_single_condition(cls, condition: str, inequality: str, num: int) -> 'PlantingCondition':
        if inequality == "이상":
            return PlantingCondition(condition=condition, min=num, max=100)
        if inequality == "이하":
            return PlantingCondition(condition=condition, min=0, max=num)


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
