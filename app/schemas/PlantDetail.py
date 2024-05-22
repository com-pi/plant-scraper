from typing import Dict
from pydantic import BaseModel


class PlantDetailSchema(BaseModel):
    name: str
    description: str
    info: Dict[str, str]