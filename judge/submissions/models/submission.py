from django.contrib.auth import get_user_model

from judge.code_tasks.models import CodeSubmissionType, CodeTask
from judge.core import models as audit_models
from django.db import models

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
        default=PROCESSING_STATE_NOT_STARTED,
    )

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.code_task.name} with {self.type.name} of {self.user.username}'
