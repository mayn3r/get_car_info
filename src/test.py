from car_info import CarInfo

license_plate = "Р888НУ97"

car = CarInfo(license_plate)
    
vin = car.vin
print('Номер:', car.car_number)
print('vin:', vin.vin)