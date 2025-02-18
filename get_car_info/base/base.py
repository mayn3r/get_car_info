from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from bs4 import BeautifulSoup
from httpx import Response
from pydantic import __version__ as pydantic_version

from get_car_info.models import CarSnapshotModel

T = TypeVar("T", bound="BaseCarInfo")
class BaseCarInfo(ABC):
    class Auth(ABC, Generic[T]):
        def __init__(self, car_info: T):
            self.car_info = car_info

        @abstractmethod
        def _get_auth_data(self, car_number: str) -> Response:
            ...

        @staticmethod
        def _parse_auth_data(response: Response) -> tuple:
            soup = BeautifulSoup(response.content, "html.parser")
            token: str = soup.find("input", {"name": "_token"})["value"].strip()
            snapshot: str = soup.find("div", {"x-init": "$wire.getDetails()"})["wire:snapshot"]
            return (token, snapshot)

    class API(ABC, Generic[T]):
        def __init__(self, car_info: T):
            self.car_info = car_info

        @abstractmethod
        def _get_result(self, car_number: str) -> Response:
            ...

        @staticmethod
        def _get_json_data(token: str, snapshot: dict) -> dict:
            return {
                "_token": token,
                "components": [
                    {
                        "snapshot": snapshot,
                        "updates": {},
                        "calls": [
                            {
                                "path": "",
                                "method": "getDetails",
                                "params": []
                            }
                        ]
                    }
                ]
            }

    def __init__(self):
        self.auth = self.Auth(self)
        self.api = self.API(self)

    @staticmethod
    def _get_model[Model](model: Model, data: any) -> Model:
        if pydantic_version.split(".")[0] == "1":
            return model.parse_obj(data)
        if pydantic_version.split(".")[0] == "2":
            return model.model_validate(data)
        raise ValueError("support pydantic version not found")
    
    @abstractmethod
    def get_data(self, car_number: str) -> CarSnapshotModel:
        ...