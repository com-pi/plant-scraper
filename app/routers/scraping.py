from fastapi import APIRouter

from app.schemas.PlantSchemas import PlantDetails, SearchPlantList
from app.services import scraper

router = APIRouter()

@router.get("/search/{keyword}", response_model=SearchPlantList)
async def scrape(keyword: str):
    result_set = scraper.getSearchResultSet(keyword)
    return result_set

@router.get("/detail/{plant_name}", response_model=PlantDetails)
async def scrape_detail(plant_name: str):
    result = scraper.scrape_detail(plant_name)
    return result

