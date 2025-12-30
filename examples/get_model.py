import asyncio

from get_car_info import AsyncCarInfo


async def main() -> None:
    car_info = AsyncCarInfo()
    number = "а123вв15"

    model = await car_info.get_data(car_number=number)
    print(model)
    
    osago = await car_info.get_osago(car_number=number)
    
    if osago is None:
        print("ОСАГО не найдено.")
    else:
        print(osago)
    

if __name__ == "__main__":
    asyncio.run(main())