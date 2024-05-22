from fastapi import FastAPI, HTTPException
from app.routers import scraping
from app.config import settings
from app.exceptions import value_error_exception_handler, http_exception_handler

app = FastAPI()

app.include_router(scraping.router)
app.add_exception_handler(ValueError, value_error_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

@app.get("/")
def root():
    return {"app_name": settings.app_name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port, reload=settings.debug)