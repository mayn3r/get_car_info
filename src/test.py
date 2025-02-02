from car_info import CarInfo


def get_data(number: str) -> None:
    car = CarInfo(number, debug=True)

    # Receiving data in Pydantic form
    data = car.get_data()

    print('Номер:', data.number)
    print('vin:', data.vin)
    print('Марка:', data.marka)
    print('Модель:', data.model)
    print('Год производства:', data.year)
    print('img:', data.image)


def get_all_data(number: str) -> None:
    car = CarInfo(number)

    # Receiving data in Pydantic form
    data = car.get_data()
    
    print('\nВся полученная информация:')
    for i in data:
        print(f'{i[0].title()}: {i[1]}')


if __name__ == '__main__':
    number = "х917ут161"
    get_all_data(number)