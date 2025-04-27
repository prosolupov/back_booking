from fastapi import HTTPException


class BackBookingException(Exception):
    detail: str = "Back Booking Exception"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(self.detail, *args, **kwargs)


class ObjectDoesExist(BackBookingException):
    detail: str = "Объект уже существует"


class ObjectNotFoundException(BackBookingException):
    detail: str = "Объект не найден"


class HotelNotFoundException(BackBookingException):
    detail: str = "Отель не найден"


class RoomNotFoundException(BackBookingException):
    detail: str = "Номер не найден"


class BookingNotFoundException(BackBookingException):
    detail: str = "Бронирования не найдены"


class UserAlreadyExistsException(BackBookingException):
    detail = "Пользователь уже существует"


class EmailNotRegisteredException(BackBookingException):
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordException(BackBookingException):
    detail = "Пароль неверный"


class BackBookingHTTPException(HTTPException):
    status_code = 500
    detail: str = None

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BackBookingHTTPException):
    status_code = 404
    detail: str = "Отель не найден"


class RoomNotFoundHTTPException(BackBookingHTTPException):
    status_code = 404
    detail: str = "Номер не найден"


class BookingNotFoundHTTPException(BackBookingHTTPException):
    status_code = 404
    detail: str = "Отсутсвуют брони"


class UserNotFoundHTTPException(BackBookingHTTPException):
    status_code = 404
    detail: str = "Пользователь не найден"

class UserAlreadyExistsHTTPException(BackBookingHTTPException):
    status_code = 409
    detail = "Пользователь уже существует"


class EmailNotRegisteredHTTPException(BackBookingHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordHTTPException(BackBookingHTTPException):
    status_code = 401
    detail = "Пароль неверный"
