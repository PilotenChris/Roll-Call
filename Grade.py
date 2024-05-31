from Course import Course


class Grade:
    def __init__(self, course: Course, grades: int):
        self.course: Course = course
        self.grades: int = grades

    def __str__(self) -> str:
        return f"Course: {self.course.name}, Grades: {self.grades}"

    @property
    def course(self) -> Course:
        return self._course

    @course.setter
    def course(self, course: Course) -> None:
        self._course: Course = course

    @property
    def grades(self) -> int:
        return self._grades

    @grades.setter
    def grades(self, grades: int) -> None:
        self._grades: int = grades
