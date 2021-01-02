from django.db import models


class CodeSubmissionType(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class CodeTask(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    code_submission_types = models.ManyToManyField(CodeSubmissionType)

    def __str__(self):
        return self.name


class TaskTest(models.Model):
    input = models.TextField()
    expected_output = models.TextField()
    code_task = models.ForeignKey(CodeTask, on_delete=models.CASCADE)