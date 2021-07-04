from django.contrib.auth import get_user_model
from django.db import models

from judge.code_tasks.models import TaskTest
from judge.core import models as audit_models
from judge.submissions.models.submission_result import SubmissionResult
from judge.submissions.models.submission_test_result_type import SubmissionTestResultType

UserModel = get_user_model()


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
        return f'''Actual - {self.actual_output}; Expected - {self.expected_output}'''
