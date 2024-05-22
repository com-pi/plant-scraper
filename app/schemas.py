from pydantic import BaseModel

class ScrapeSchema(BaseModel):
    name: str
