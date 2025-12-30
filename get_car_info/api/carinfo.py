import json

from httpx import AsyncClient, Client

from ..base import BaseCarInfo, ModeLiteral
from ..exceptions import CarNotFound
from ..models import CarSnapshotModel, OsagoModel


class CarInfo(BaseCarInfo):
    class Auth(BaseCarInfo.Auth["CarInfo"]):
        def _get_auth_data(self, obj: str, mode: ModeLiteral = "gosnumber") -> tuple:
            
            res = self.car_info._client.get(f"order/create?object={obj}&mode={mode}")
            return self._parse_auth_data(res)

    class API(BaseCarInfo.API["CarInfo"]):
        def _get_result(self, obj: str, mode: ModeLiteral) -> dict:
            token, snapshot = self.car_info.auth._get_auth_data(obj, mode) # type: ignore
            res = self.car_info._client.post("livewire/update", json=self._get_json_data(token, snapshot))
            res = res.json().get("components")[0].get("snapshot")
            return json.loads(res)

    def __init__(self) -> None:
        super().__init__()
        self._client = Client(base_url="https://vinvision.ru/")

    def get_data(self, *, car_number: str | None = None, vin: str | None = None) -> type[CarSnapshotModel]:
        error_msg = "Должен быть указан или гос номер, или vin автомобиля"
        assert any((car_number, vin)), error_msg
        assert not all((car_number, vin)), error_msg
        
        if car_number:
            mode = "gosnumber"
            
        elif vin:
            mode = "vin"
        
        obj: str = (car_number or vin)   # type: ignore
        res = self.api._get_result(obj=obj, mode=mode)

        try:
            first_result = res.get("data").get("details")[0].get("result")[0] # type: ignore
        except Exception:
            raise CarNotFound from None
        res = {i.lower(): k for i, k in first_result.items()}

        return self._get_model(CarSnapshotModel, res)
    
    def get_osago(self, car_number: str) -> type[OsagoModel] | None:
        """ Попытка получения данных ОСАГО """
        
        url = "https://www.sravni.ru/proxy-osagoinsurance/getPrevCalculationOrPolicy/"
        data = {"carNumber": car_number.upper(), "isShortProlongation": True}
        
        response = Client().post(url=url, data=data).json()
        
        if len(response.keys()) == 1:
            return None
        
        return self._get_model(OsagoModel, response)
        


class AsyncCarInfo(BaseCarInfo):
    class Auth(BaseCarInfo.Auth["AsyncCarInfo"]):
        async def _get_auth_data(self, obj: str, mode: ModeLiteral = "gosnumber") -> tuple:
            
            res = await self.car_info._client.get(f"order/create?object={obj}&mode={mode}")
            return self._parse_auth_data(res)

    class API(BaseCarInfo.API["AsyncCarInfo"]):
        async def _get_result(self, obj: str, mode: ModeLiteral) -> dict:
            token, snapshot = await self.car_info.auth._get_auth_data(obj, mode) # type: ignore
            res = await self.car_info._client.post("livewire/update", json=self._get_json_data(token, snapshot))
            res = res.json().get("components")[0].get("snapshot")
            return json.loads(res)

    def __init__(self) -> None:
        super().__init__()
        self._client = AsyncClient(base_url="https://vinvision.ru/")

    async def get_data(self, *, car_number: str | None = None, vin: str | None = None) -> type[CarSnapshotModel]:
        error_msg = "Должен быть указан или гос номер, или vin автомобиля"
        assert any((car_number, vin)), error_msg
        assert not all((car_number, vin)), error_msg
        
        if car_number:
            mode = "gosnumber"
            
        elif vin:
            mode = "vin"
        
        obj: str = (car_number or vin)   # type: ignore
        res = await self.api._get_result(obj=obj, mode=mode) # type: ignore

        try:
            first_result = res.get("data").get("details")[0].get("result")[0]
        except Exception:
            raise CarNotFound from None
        res = {i.lower(): k for i, k in first_result.items()}

        return self._get_model(CarSnapshotModel, res)
    
    async def get_osago(self, car_number: str) -> type[OsagoModel] | None:
        """ Попытка получения данных ОСАГО """
        
        url = "https://www.sravni.ru/proxy-osagoinsurance/getPrevCalculationOrPolicy/"
        data = {"carNumber": car_number.upper(), "isShortProlongation": True}
        
        response = await AsyncClient().post(url=url, data=data)
        response = response.json()
        
        if len(response.keys()) == 1:
            return None
        
        return self._get_model(OsagoModel, response)