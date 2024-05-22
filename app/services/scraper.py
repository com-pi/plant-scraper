from typing import Dict

import requests
from fastapi import HTTPException
from bs4 import BeautifulSoup

from app.schemas.PlantDetail import PlantDetailSchema

base_search_url = "https://drfull.im/api/search-plants"
base_detail_url = "https://drfull.im/plants/detail"


def scrape_detail(plant_name: str) -> PlantDetailSchema:
    url = f"{base_detail_url}/{plant_name}"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    infoDiv = soup.select_one("#layout_body .plantDetail__page-flex .plants-simpleinfo-section")
    if not infoDiv:
        raise ValueError("Could not find the infoDiv")

    name = infoDiv.select_one(".simpleinfo-title .simpleinfo__title-wrap h1").text.strip()
    description = infoDiv.select_one(".simpleinfo-title h3").text

    info: Dict[str, str] = {}
    col = ["물주기", "광도", "습도", "학명"]

    info_items = infoDiv.select(".simpleinfo-table .table-item")
    for index, info_item in enumerate(info_items):
        info1 = info_item.find("h1").text.strip()
        info2 = info_item.find("h2").text.strip()
        info[col[index]] = f"{info1}, {info2}"

    return PlantDetailSchema(
        name = name,
        description = description,
        info = info
    )


def getResultSet(keyword: str):
    url = f"{base_search_url}?keyword={keyword}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
