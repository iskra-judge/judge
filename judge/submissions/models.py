from django.db import models

from judge.code_tasks.models import CodeSubmissionType, CodeTask, TaskTest


class Submission(models.Model):
    PROCESSING_STATE_NOT_STARTED = "NOT_STARTED"
    PROCESSING_STATE_ENQUEUED_FOR_PROCESSING = "ENQUEUE_FOR_PROCESSING"
    PROCESSING_STATE_PROCESSED = "PROCESSED"
    PROCESSING_STATE_CHOICES = (
        (PROCESSING_STATE_NOT_STARTED, PROCESSING_STATE_NOT_STARTED),
        (PROCESSING_STATE_ENQUEUED_FOR_PROCESSING, PROCESSING_STATE_ENQUEUED_FOR_PROCESSING),
        (PROCESSING_STATE_PROCESSED, PROCESSING_STATE_PROCESSED),
    )

    code = models.TextField()
    type = models.ForeignKey(CodeSubmissionType, on_delete=models.CASCADE)
    code_task = models.ForeignKey(CodeTask, on_delete=models.CASCADE)
    processing_state = models.CharField(
        max_length=len(PROCESSING_STATE_ENQUEUED_FOR_PROCESSING),
        choices=PROCESSING_STATE_CHOICES,
        default=PROCESSING_STATE_NOT_STARTED
    )


class SubmissionTestResultType(models.Model):
    CORRECT_ANSWER = 'Correct Answer'
    WRONG_ANSWER = 'Wrong Answer'
    EXECUTION_ERROR = 'Execution Error'
    UNKNOWN_TYPE = 'Unknown'
    TYPES = (
        ('CA', CORRECT_ANSWER),
        ('WA', WRONG_ANSWER),
        ('EE', EXECUTION_ERROR),
        ('UT', UNKNOWN_TYPE),
    )

    name = models.CharField(
        max_length=2,
        choices=TYPES,
        default=UNKNOWN_TYPE,
    )

    def __str__(self):
        return self.name


class SubmissionTestResult(models.Model):
    expected_output = models.TextField()
    actual_output = models.TextField()
    execution_time = models.FloatField(null=True, blank=True)
    execution_memory = models.FloatField(null=True, blank=True)
    task_test = models.ForeignKey(TaskTest, on_delete=models.CASCADE)
    type = models.ForeignKey(SubmissionTestResultType, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type}'


class SubmissionResult(models.Model):
    code_submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    is_retest = models.BooleanField(default=False)
    total_score = models.IntegerField()

    def __str__(self):
        return str(self.total_score)
