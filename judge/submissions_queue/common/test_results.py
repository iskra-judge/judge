from enum import Enum


class TestResultType(Enum):
    CorrectAnswer = 1
    WrongAnswer = 2
    RuntimeError = 3


class TestResult:
    def __init__(self, is_successful, type, output):
        self.is_successful = is_successful
        self.type = type
        self.output = output

    @property
    def points(self):
        return int(self.is_successful) * 10

    def __repr__(self):
        return ';'.join(f'{key}={value}' for (key, value) in self.__dict__.items())
