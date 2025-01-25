from pydantic import BaseModel
from typing import Union, Optional


class CarSnapshotModel(BaseModel):
    vin: str
    number: str
    marka: Optional[str]
    model: Optional[str]
    year: int
    color: Optional[str]
    volume: Union[int, float]
    horsepower: Union[int, float]