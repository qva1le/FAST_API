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