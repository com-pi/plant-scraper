from typing import List

import httpx
import requests
from fastapi import HTTPException
from bs4 import BeautifulSoup

from app.schemas.PlantSchemas import PlantDetails, PlantAttribute, SearchPlantResult, SearchPlantList

base_search_url = "https://drfull.im/api/search-plants"
base_detail_url = "https://drfull.im/plants/detail"


def scrape_detail_old_version(soup) -> PlantDetails:
    infoDiv = soup.select_one("#layout_body .plantDetail__page-flex .plants-simpleinfo-section")
    if not infoDiv:
        raise ValueError("Could not find the infoDiv")
    name = infoDiv.select_one(".simpleinfo-title .simpleinfo__title-wrap h1").text.strip()
    description = infoDiv.select_one(".simpleinfo-title h3").text
    scientific_name = ""

    info: List[PlantAttribute] = []
    col = ["물주기", "광도", "습도", "학명"]

    info_items = infoDiv.select(".simpleinfo-table .table-item")
    for index, info_item in enumerate(info_items):
        info1 = info_item.find("h1").text.strip()
        info1 = info_item.find("h1").text.strip()
        info2 = info_item.find("h2").text.strip()
        if (index < 3):
            info.append(PlantAttribute(name=col[index], info1=info1, info2=info2))
        else:
            scientific_name = info2

    image_source = soup.select(
        "#plantDetail__page > div.layout__pc > div > section.plantDetail-slide-section > div > div.swiper-wrapper > div > img")

    image_urls = [
        image_source.attrs["src"]
        for image_source in image_source
    ]

    return PlantDetails(
        name=name,
        description=description,
        scientific_name=scientific_name,
        info=info,
        image_urls=image_urls
    )


def scrape_detail_new_version(soup) -> PlantDetails:
    scientific_name = soup.select_one("#plantDetail__page > div > div > div > p").text.strip()
    name = soup.select_one(
        "#plantDetail__page > div > div > div > section.plantDetail__section > div > h1").text.strip()
    description = soup.select_one(
        "#plantDetail__page > div > div > div > section.plants-simpleinfo-section > p").text.strip()
    info: List[PlantAttribute] = []
    col = ["물주기", "광도", "습도", "온도"]

    info_items = soup.select_one(
        "#plantDetail__page > div > div > div > section.plants-simpleinfo-section > div > ul").find_all("li")
    for index, info_item in enumerate(info_items):
        info1 = info_item.select_one(".table-item-title").text.strip()
        info2 = info_item.select_one(".table-item-desc").text.strip()
        info.append(PlantAttribute(name=col[index], info1=info1, info2=info2))

    image_source = soup.select(
        "#plantDetail__page > div > div > section > div > div > div > div.swiper-wrapper > div > img")
    image_urls = [
        image_source.attrs["src"]
        for image_source in image_source
    ]

    return PlantDetails(
        name=name,
        description=description,
        scientific_name=scientific_name,
        info=info,
        image_urls=image_urls
    )


async def scrape_detail(plant_name: str) -> PlantDetails:
    url = f"{base_detail_url}/{plant_name}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

    if soup.find("html") is None:
        raise HTTPException(
            status_code=404,
            detail=f"해당 식물의 정보가 없습니다. : {plant_name}"
        )

    if soup.select_one("#plantDetailV4__page"):
        return scrape_detail_new_version(soup)
    else:
        return scrape_detail_old_version(soup)


async def getSearchResultSet(keyword: str) -> SearchPlantList:
    url = f"{base_search_url}?keyword={keyword}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            result = response.json()

            if "data" not in result or len(result["data"]) == 0:
                raise HTTPException(
                    status_code=404,
                    detail=f"검색 결과가 없습니다 : {keyword}"
                )

            plants = [
                SearchPlantResult(
                    name=plant["plantname_korean"],
                    thumbnail_url=plant["thumbnail"]
                )
                for plant in result["data"]
            ]

            return SearchPlantList(
                results=plants
            )

    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
