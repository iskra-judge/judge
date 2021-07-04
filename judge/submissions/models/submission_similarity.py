from django.db import models

from judge.submissions.models.submission import Submission


class SubmissionSimilarity(models.Model):
    jaccard_similarity = models.IntegerField()
    lcs_similarity = models.IntegerField()
    cosine_similarity = models.IntegerField()
    submission1 = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="submissions1")
    submission2 = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="submissions2")

    class Meta:
        verbose_name_plural = 'submission similarities'
