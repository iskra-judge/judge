from django.contrib.auth import get_user_model
from django.db import models

from judge.code_tasks.models import CodeSubmissionType, CodeTask, TaskTest
from judge.core import models as audit_models

UserModel = get_user_model()


class Submission(audit_models.AuditModel):
    PROCESSING_STATE_NOT_STARTED = "NOT_STARTED"
    PROCESSING_STATE_ENQUEUED_FOR_JUDGING = "ENQUEUE_FOR_JUDGING"
    PROCESSING_STATE_JUDGED = "JUDGED"
    PROCESSING_STATE_JUDGING_IN_PROGRESS = "JUDGING_IN_PROGRESS"

    PROCESSING_STATE_CHOICES = (
        (PROCESSING_STATE_NOT_STARTED, PROCESSING_STATE_NOT_STARTED),
        (PROCESSING_STATE_ENQUEUED_FOR_JUDGING, PROCESSING_STATE_ENQUEUED_FOR_JUDGING),
        (PROCESSING_STATE_JUDGING_IN_PROGRESS, PROCESSING_STATE_JUDGING_IN_PROGRESS),
        (PROCESSING_STATE_JUDGED, PROCESSING_STATE_JUDGED),
    )

    code = models.TextField()
    type = models.ForeignKey(CodeSubmissionType, on_delete=models.CASCADE)
    code_task = models.ForeignKey(CodeTask, on_delete=models.CASCADE)
    processing_state = models.CharField(
        max_length=len(PROCESSING_STATE_ENQUEUED_FOR_JUDGING),
        choices=PROCESSING_STATE_CHOICES,
        default=PROCESSING_STATE_NOT_STARTED
    )

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.code_task.name} with {self.type.name} of {self.user.username}'


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


class SubmissionSimilarity(models.Model):
    jaccard_similarity = models.IntegerField()
    lcs_similarity = models.IntegerField()
    cosine_similarity = models.IntegerField()
    submission1 = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="submissions1")
    submission2 = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="submissions2")


class SubmissionResult(audit_models.AuditModel):
    code_submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    is_retest = models.BooleanField(default=False)
    total_score = models.IntegerField()

    def __str__(self):
        return str(self.total_score)


class SubmissionTestResult(audit_models.AuditModel):
    expected_output = models.TextField()
    actual_output = models.TextField()
    execution_time = models.FloatField(null=True, blank=True)
    execution_memory = models.FloatField(null=True, blank=True)
    is_zero_test = models.BooleanField(default=False)
    task_test = models.ForeignKey(TaskTest, on_delete=models.CASCADE)
    test_result_type = models.ForeignKey(SubmissionTestResultType, on_delete=models.CASCADE)
    submission_result = models.ForeignKey(SubmissionResult, on_delete=models.CASCADE)

    def __str__(self):
        return f'''A{self.actual_output}
E{self.expected_output}'''
