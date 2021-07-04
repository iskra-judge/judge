from django.db import models


class SubmissionTestResultType(models.Model):
    CORRECT_ANSWER = 'Correct Answer'
    WRONG_ANSWER = 'Wrong Answer'
    EXECUTION_ERROR = 'Execution Error'
    UNKNOWN_TYPE = 'Unknown'
    TIME_LIMIT = 'Time Limit'
    MEMORY_LIMIT = 'Memory Limit'

    TYPES = (
        (CORRECT_ANSWER, CORRECT_ANSWER),
        (WRONG_ANSWER, WRONG_ANSWER),
        (EXECUTION_ERROR, EXECUTION_ERROR),
        (UNKNOWN_TYPE, UNKNOWN_TYPE),
        (TIME_LIMIT, TIME_LIMIT),
        (MEMORY_LIMIT, MEMORY_LIMIT),
    )

    name = models.CharField(
        max_length=max(len(x) for x in (CORRECT_ANSWER, WRONG_ANSWER, EXECUTION_ERROR, UNKNOWN_TYPE)),
        choices=TYPES,
        default=UNKNOWN_TYPE,
    )

    @staticmethod
    def wrong_answer():
        return SubmissionTestResultType.objects.filter(name=SubmissionTestResultType.WRONG_ANSWER) \
            .first()

    @staticmethod
    def correct_answer():
        return SubmissionTestResultType.objects.filter(name=SubmissionTestResultType.CORRECT_ANSWER) \
            .first()

    @staticmethod
    def execution_error():
        return SubmissionTestResultType.objects.filter(name=SubmissionTestResultType.EXECUTION_ERROR) \
            .first()

    @staticmethod
    def time_limit_error():
        return SubmissionTestResultType.objects.filter(name=SubmissionTestResultType.TIME_LIMIT) \
            .first()

    @staticmethod
    def memory_limit_error():
        return SubmissionTestResultType.objects.filter(name=SubmissionTestResultType.MEMORY_LIMIT) \
            .first()

    def __str__(self):
        return self.name
