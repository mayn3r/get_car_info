class CarNotFound(BaseException):
    __module__ = object.__module__
    
    def __init__(self):
        super().__init__("I doesn't found your car...")


# class OsagoNotFound(BaseException):
#     __module__ = object.__module__
    
#     def __init__(self):
#         super().__init__("Не удалось найти данные ОСАГО")