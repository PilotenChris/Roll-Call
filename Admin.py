from Person import Person


class Admin(Person):
    def __init__(self, id: int, name: str, surname: str, birthdate: str, email: str, uniEmail: str):
        super().__init__(id, name, surname, birthdate, email, uniEmail)

    def __str__(self) -> str:
        return super().__str__()
