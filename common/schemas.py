
from pydantic import BaseModel, ConfigDict

class Listing(BaseModel):
    model_config = ConfigDict(extra="allow")
    item_id: str
    marketplace: str
    title: str
    price: int | None
    currency: str
    url: str
