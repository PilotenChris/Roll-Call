class Person:
    def __init__(self, id: int, name: str, surname: str, birthdate: str, email: str, uniEmail: str) -> None:
        self.id: int = id
        self.name: str = name
        self.surname: str = surname
        self.birthdate: str = birthdate
        self.email: str = email
        self.uniEmail: str = uniEmail

    def __str__(self) -> str:
        return (f"ID: {self._id}, First name: {self._name}, Surname: {self._surname}, Birthdate: {self._birthdate}, "
                f"Email: {self._email}, University email: {self._uniEmail}")

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int) -> None:
        self._id: int = id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name: str = name

    @property
    def surname(self) -> str:
        return self._surname

    @surname.setter
    def surname(self, surname: str) -> None:
        self._surname: str = surname

    @property
    def birthdate(self) -> str:
        return self._birthdate

    @birthdate.setter
    def birthdate(self, birthdate: str) -> None:
        self._birthdate: str = birthdate

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        self._email: str = email

    @property
    def uniEmail(self) -> str:
        return self._uniEmail

    @uniEmail.setter
    def uniEmail(self, uniEmail: str) -> None:
        self._uniEmail: str = uniEmail
