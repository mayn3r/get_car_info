
from pydantic import BaseModel


class CarSnapshotModel(BaseModel):
    vin: str
    number: str
    marka: str | None
    model: str | None
    year: int
    color: str | None
    volume: int | float
    horsepower: int | float
    image: str | None
    