from django.db import models

from judge.core import models as audit_models
from judge.submissions.models.submission import Submission


class SubmissionResult(audit_models.AuditModel):
    code_submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    is_retest = models.BooleanField(default=False)
    total_score = models.IntegerField()

    def __str__(self):
        return str(self.total_score)
