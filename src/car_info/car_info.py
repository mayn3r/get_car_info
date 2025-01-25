import requests
import json
import re

from bs4 import BeautifulSoup
from typing import Dict, Optional, Union

from pydantic_core._pydantic_core import ValidationError
from json.decoder import JSONDecodeError

from .models import CarSnapshotModel


class CarInfo:
    """
    Getting information about a car using Russian state license plates
    
    Args:
        number -> The state number of the car, format: A001AA01 (The letters must be written in Cyrillic.)
    """
    
    def __init__(self, number: str, **kwargs):
        self.car_number: str = number.replace(' ', '').strip().upper()
        self._debug: bool = bool(kwargs.get('debug', 0))
        
        self._data = self.Data(self)
        self._model: Optional[CarSnapshotModel] = None
    
    
    def get_data(self) -> Union[CarSnapshotModel, Dict]:
        """ Converting data from 'snapshot' to pydantic model """
        if self._model:
            return self._model
        
        # Half of the basic information about the car is in the form of a dictionary, 
        # where the name of the key is written with a capital letter
        try:
            first_result: Dict = self._data._snapshot['data']['details'][0]['result'][0]
        except KeyError:
            return None
        
        # Changing the case in the key name to a small one
        result: Dict = {i.lower(): k for i, k in first_result.items()}
        
        try:
            # Creating a pydantic model with the received data
            self._model = CarSnapshotModel.model_validate(result)
        except ValidationError:
            # In case of errors with Pydantic, the function returns a dictionary with data.
            if self._debug:
                print('[DEBUG] -> Warning! An error occurred when trying to translate a JSON object to the Pydantic model. The object is returned as a dictionary')
            
            self._model = result
            
        return self._model
        
    
    class Data:
        """
        Getting a vin number by a government number using parsing
        """
        
        def __init__(self, car_info_object: "CarInfo"):
            self.car_info_obj: "CarInfo" = car_info_object
            
            # Creating a new session
            self.session = requests.Session()
            self.session.headers.update(self._get_headers())
            
            # Receiving cookies
            self._cookies: Dict[str] = self._get_cookies()
            
            # Immediately upon initialization of the class, we get the vin number
            self._snapshot: str = self.get_result()
        
        
        def __str__(self):
            """ When outputting an object of the Vin class, we will get the vin number of the car. """
            
            return 'Vin("%s")' % self.vin


        def __repr__(self):
            return 'CarInfo(number="%s").vin' % self.car_info_obj.car_number
        
        
        def _get_headers(self) -> Dict:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36',
            }
            
            return headers

        
        def _get_cookies(self) -> Dict:
            """ Receiving cookies after the first request to the main page """

            # Sending a GET request to the home page to receive cookies
            response = self.session.get('https://vinvision.ru/')
            cookies = response.cookies

            return cookies.get_dict()
            
            
        def _get_auth_data(self) -> tuple:
            """ Getting a 'token' and a 'snapshot' are necessary to generate a request when receiving a vin

            Returns:
                *It is returned as a tuple, the first element of which is a 'token', the second is a 'snapshot'.
            """
            
            number: str = self.car_info_obj.car_number
            
            url = "https://vinvision.ru/order/create?object={}&mode=gosnumber".format(number)
            
            # Sending a request to get an HTML section of code with the required 'token' and 'snapshot'
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'lxml')
            
            token: str = soup.find('input', {'name': '_token'})['value'].strip()
            snapshot: str = soup.find('div', {"x-init": "$wire.getDetails()"})['wire:snapshot']
            
            return (token, snapshot)
            
            
        def get_result(self) -> Dict:
            """ Getting a data, you do not need to enter the state number of the car, because the received token is responsible for it.
            """
            
            # 
            token, snapshot = self._get_auth_data()
                    
            # Data required when generating a request for a vin number  
            json_data = {
                '_token': token,
                'components': [
                    {
                        'snapshot': f'{snapshot}',
                        'updates': {},
                        'calls': [
                            {
                                'path': '',
                                'method': 'getDetails',
                                'params': []
                            }
                        ]
                    }
                ]
            }
            
            url = 'https://vinvision.ru/livewire/update'
            
            # Sending a POST request to receive a response containing the vehicle's vin number
            response = self.session.post(
                url=url, 
                json=json_data, 
                cookies=self._cookies
            )
            
            error = ValueError('Не удалось получить данные по этому гос номеру')
            
            try:
                # We are trying to pull a snapshot from the response,
                # if the response is not converted to a JSON object, then an error has occurred.
                snapshot: Dict = json.loads(response.json()['components'][0]['snapshot'])
                
                if not snapshot['data']['details'][0].get('result'):
                    if self.car_info_obj._debug:
                        print(f'[DEBUG] -> {snapshot=}')
                        
                    raise error
                
            except (JSONDecodeError, IndexError):
                raise error
            
            return snapshot


