from fastapi import APIRouter
from app.services import scraper

router = APIRouter()

@router.get("/search/{keyword}")
async def scrape(keyword: str):
    result_set = scraper.getResultSet(keyword)
    return result_set

@router.get("/detail/{plant_name}")
async def scrape_detail(plant_name: str):
    result = scraper.scrape_detail(plant_name)
    return result

