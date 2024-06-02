from fastapi import APIRouter

from app.schemas.PlantSchemas import PlantDetails, SearchPlantList
from app.services import scraper

router = APIRouter()

@router.get("/search/{keyword}", response_model=SearchPlantList)
async def scrape(keyword: str):
    return await scraper.get_search_result_set(keyword)

@router.get("/detail/{plant_name}", response_model=PlantDetails)
async def scrape_detail(plant_name: str):
    return await scraper.get_detail_info(plant_name)

