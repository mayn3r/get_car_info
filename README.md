<h1>Получение VIN по гос номеру</h1>

<h3>Использование:</h3>

```python
from car_info import CarInfo

car = CarInfo('Е005КХ05')
    
vin = car.vin.vin
print('Номер:', car.car_number)
print('Vin:', vin)
```

При указании гос номера необходимо использовать кириллицу!
<hr>

Примечание:

> `car.vin` является объектом `CarInfo.Vin`, а не самим VIN номером.
<br>
Чтобы получить VIN, используйте `CarInfo.Vin.vin`.
<br>
Для кода выше будет характерно `car.vin.vin`

<hr>
