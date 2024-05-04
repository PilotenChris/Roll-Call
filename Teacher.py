from Person import Person
from Course import Course


class Teacher(Person):
    def __init__(self, id: int, name: str, surname: str, birthdate: str, email: str, uniEmail: str,
                 courses: list[Course]):
        super().__init__(id, name, surname, birthdate, email, uniEmail)
        self.courses: list[Course] = courses

    def __str__(self) -> str:
        course: list[str] = []
        for i in self._courses:
            course.append(f"{i.id} {i.name}, ")
        return f"{super().__str__()}, Courses: {''.join(course)}"

    @property
    def courses(self) -> list[Course]:
        return self._courses

    @courses.setter
    def courses(self, courses: list[Course]) -> None:
        self._courses: list[Course] = courses
