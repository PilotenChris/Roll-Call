from Person import Person
from Course import Course
from Grade import Grade


class Student(Person):
    def __init__(self, id: int, name: str, surname: str, birthdate: str, email: str, uniEmail: str, degree: str,
                 courses: list[Course], grades: list[Grade]):
        super().__init__(id, name, surname, birthdate, email, uniEmail)
        self.degree: str = degree
        self.courses: list[Course] = courses
        self.grades: list[Grade] = grades

    def __str__(self) -> str:
        course: list[str] = []
        for i in self._courses:
            course.append(f"{i.id} {i.name}")

        grade: list[str] = []
        for g in self._grades:
            grade.append(f"{g.course.name}: {g.grades}")

        return f"{super().__str__()}, Degree: {self._degree}, Courses: {', '.join(course)}, Grades: {', '.join(grade)}"

    @property
    def degree(self) -> str:
        return self._degree

    @degree.setter
    def degree(self, degree: str) -> None:
        self._degree: str = degree

    @property
    def courses(self) -> list[Course]:
        return self._courses

    @courses.setter
    def courses(self, courses: list[Course]) -> None:
        self._courses: list[Course] = courses

    @property
    def grades(self) -> list[Grade]:
        return self._grades

    @grades.setter
    def grades(self, grades: list[Grade]) -> None:
        self._grades: list[Grade] = grades
