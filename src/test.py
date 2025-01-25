from car_info import CarInfo

number = "а005аа05"

car = CarInfo(number=number)

# Receiving data in Pydantic form
data = car.get_data()

print('Номер:', data.number)
print('vin:', data.vin)
print('Марка:', data.marka)
print('Модель:', data.model)
print('Год производства:', data.year)


# # # # # # # # # # # # # # # # # # # # 
# print('\nВся полученная информация:')
# for i in data:
#     print(f'{i[0].title()}: {i[1]}')