from car_info import CarInfo


def main(number: str) -> None:
    car = CarInfo(number)

    # Receiving data in Pydantic form
    data = car.get_data()

    print('Номер:', data.number)
    print('vin:', data.vin)
    print('Марка:', data.marka)
    print('Модель:', data.model)
    print('Год производства:', data.year)
    print('img:', data.image)


    # # # # # # # # # # # # # # # # # # # # 
    # print('\nВся полученная информация:')
    # for i in data:
    #     print(f'{i[0].title()}: {i[1]}')


number = "Р123НУ97"
    
main(number)