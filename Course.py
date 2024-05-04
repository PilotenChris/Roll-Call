from Teacher import Teacher
from Student import Student


class Course:
    def __init__(self, id: int, name: str, teachers: list[Teacher], students: list[Student]):
        self.id: int = id
        self.name: str = name
        self.teachers: list[Teacher] = teachers
        self.students: list[Student] = students

    def __str__(self) -> str:
        return f"ID: {self._id}, Course name: {self._name}, Teachers: {self._teachers}, Students: {self._students}"

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
    def teachers(self) -> list[Teacher]:
        return self._teachers

    @teachers.setter
    def teachers(self, teachers: list[Teacher]) -> None:
        self._teachers: list[Teacher] = teachers

    @property
    def students(self) -> list[Student]:
        return self._students

    @students.setter
    def students(self, students: list[Student]) -> None:
        self._students: list[Student] = students
