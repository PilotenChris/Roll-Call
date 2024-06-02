class Course:
    def __init__(self, id: int, name: str, passing_grade: int, active_status: int):
        self.id: int = id
        self.name: str = name
        self.passing_grade: int = passing_grade
        self.active_status: int = active_status

    def __str__(self) -> str:
        return f"ID: {self.id}, Course name: {self.name}, Passing grade: {self.passing_grade}, Active status: {self.active_status}"

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
    def passing_grade(self) -> int:
        return self._passing_grade

    @passing_grade.setter
    def passing_grade(self, passing_grade: int) -> None:
        self._passing_grade: int = passing_grade

    @property
    def active_status(self) -> int:
        return self._active_status

    @active_status.setter
    def active_status(self, active_status: int) -> None:
        self._active_status: int = active_status
