from fastapi import APIRouter

router = APIRouter()

@router.get("/scrape/{keyword}", response_model=)