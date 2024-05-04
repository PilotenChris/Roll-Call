from Course import Course


class Grade:
    def __init__(self, course: Course, grades: list[dict]):
        self.course: Course = course
        self.grades: list[dict] = grades

    def __str__(self) -> str:
        return f"Course: {self._course}, Grades: {self._grades}"

    @property
    def course(self) -> Course:
        return self._course

    @course.setter
    def course(self, course: Course) -> None:
        self._course: Course = course

    @property
    def grades(self) -> list[dict]:
        return self._grades

    @grades.setter
    def grades(self, grades: list[dict]) -> None:
        self._grades: list[dict] = grades
