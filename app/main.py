from fastapi import FastAPI
from app.routers import scraping
from app.config import settings

app = FastAPI()

app.include_router(scraping.router)

@app.get("/")
def root():
    return {"app_name": settings.app_name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port, reload=settings.debug)