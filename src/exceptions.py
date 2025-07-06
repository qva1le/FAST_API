from fastapi import HTTPException


class NabronorivalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronorivalException):
    detail = "Объект не найден"

class AllRoomsAreBookedException(NabronorivalException):
    detail = "Не осталось свободных номеров"

class UserIsAlreadyExists(NabronorivalException):
    detail = "Такой пользователь уже существует"

class DatesAreIncorrect(NabronorivalException):
    detail = "Установлены неправильные даты"

class HotelDoesNotExist(NabronorivalException):
    detail = "Такого отеля не существует"

class RoomDoesNotExist(NabronorivalException):
    detail = "Такого номера не существует"

class HotelNotFoundException(NabronorivalException):
    detail = "Такого отеля не существует"



class NabrovirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

#наследуем
class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"

class HotelNotFoundHTTPException(HotelNotFoundException):
    detail = "Такого отеля не существует"