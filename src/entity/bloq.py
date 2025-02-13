from pydantic import BaseModel

class Bloq(BaseModel):
    id: str
    title: str
    address: str