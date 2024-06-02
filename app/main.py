from fastapi import FastAPI, HTTPException

from app.config import settings
from app.exceptions import http_exception_handler
from app.routers import scraping

app = FastAPI()

app.include_router(scraping.router)
app.add_exception_handler(HTTPException, http_exception_handler)

@app.get("/")
def root():
    return {"app_name": settings.app_name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port, reload=settings.debug)