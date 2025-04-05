<h1>Получение информации по госномеру</h1>

[![image](https://img.shields.io/pypi/v/get_car_info.svg)](https://pypi.org/project/get-car-info)
[![Downloads](https://img.shields.io/pypi/dm/get-car-info)](https://pypistats.org/packages/get-car-info)
[![image](https://img.shields.io/pypi/pyversions/get-car-info.svg)](https://pypi.org/project/get-car-info)

<h2>Установка:</h2>
<p>Через pip:</p>

```shell
pip install get-car-info
```
<p>Через uv:</p>

```shell
uv add get-car-info
```
<h2>Использование:</h2>

```python
from get_car_info import CarInfo

# Укажите российский автомобильный номер в формате А123АА97
car = CarInfo()
data = car.get_data("Е005КХ05")

# Некоторая информация
print('Номер:', data.number)
print('vin:', data.vin)
print('Марка:', data.marka)
print('Модель:', data.model)
print('Год производства:', data.year)
```

При указании гос номера необходимо использовать кириллицу!
<hr>

> `car.get_data()` возвращает Pydantic объект, где описаны характеристики автомобиля.
<hr>

###### • Вся полученная информация находится в общем доступе. Данные получены с помощью <a href="https://vinvision.ru/">www.vinvision.ru</a>
