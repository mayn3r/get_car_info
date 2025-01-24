import requests
import re

from bs4 import BeautifulSoup
from typing import Dict


class CarInfo:
    """Getting information about a car using Russian state license plates
    
    Args:
        number -> The state number of the car, format: A001AA01 (The letters must be written in Cyrillic.)
    """
    def __init__(self, number: str):
        self.car_number = number.strip().upper()
        
        self.vin = self.Vin(self)
    
    
    class Vin:
        """Getting a vin number by a government number using parsing
        """
        
        def __init__(self, car_info_object: "CarInfo"):
            self.car_info_obj: 'CarInfo' = car_info_object
            
            # Creating a new session
            self.session = requests.Session()
            
            # Receiving cookies
            self._cookies: Dict[str] = self._get_cookies()
            self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36'}
            
            # Immediately upon initialization of the class, we get the vin number
            self.vin: str = self.get_vin()
        
        
        def __str__(self):
            """ When outputting an object of the Vin class, we will get the vin number of the car. """
            if self.vin is None:
                self.vin = self.get_vin()
            
            return self.vin

        
        def _get_cookies(self) -> Dict:
            """ Receiving cookies after the first request to the main page """
            
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'ru,en;q=0.9',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Chromium";v="130", "YaBrowser";v="24.12", "Not?A_Brand";v="99", "Yowser";v="2.5"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36',
            }

            # Sending a GET request to the home page to receive cookies
            response = self.session.get('https://vinvision.ru/', headers=headers)
            cookies = response.cookies

            return cookies.get_dict()
            
            
        def _get_data(self) -> tuple:
            """ Getting a 'token' and a 'snapshot' are necessary to generate a request when receiving a vin

            Returns:
                *It is returned as a tuple, the first element of which is a 'token', the second is a 'snapshot'.
            """
            
            number: str = self.car_info_obj.car_number
            
            url = "https://vinvision.ru/order/create?object={}&mode=gosnumber".format(number)
            
            # Sending a request to get an HTML section of code with the required 'token' and 'snapshot'
            response = self.session.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'lxml')
            
            token: str = soup.find('input', {'name': '_token'})['value'].strip()
            snapshot: str = soup.find('div', {"x-init": "$wire.getDetails()"})['wire:snapshot']
            
            return (token, snapshot)
            
            
        def get_vin(self) -> str:
            """ Getting a vin number, you do not need to enter the state number of the car, because the received token is responsible for it.

            Returns:
                _type_: _description_
            """
            
            # 
            token, snapshot = self._get_data()
                    
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
                headers=self.headers, 
                cookies=self._cookies
            )
            
            try:
                # We are trying to pull a snapshot from the response,
                # if the response is not converted to a JSON object, then an error has occurred.
                snapshot = response.json()['components'][0]['snapshot']
            except:
                raise ValueError('Не удалось получить VIN по этому гос номеру')
            else:
                # We get a lot of extra stuff in the response, and we find and pull the vin out of this garbage.
                vin: str = re.findall(r'"vin":"([a-zA-Z0-9]*)"', snapshot)[0]
                
                return vin


