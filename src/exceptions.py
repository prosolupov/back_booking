class BackBookingException(Exception):
    detail: str = "Back Booking Exception"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(self.detail, *args, **kwargs)


class ObjectDoesExist(BackBookingException):
    detail: str = "Объект уже существует"

class ObjectNotFoundException(BackBookingException):
    detail:str = "Объект не найден"