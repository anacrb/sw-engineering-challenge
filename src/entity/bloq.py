from pydantic import BaseModel, ConfigDict


class Bloq(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    address: str
