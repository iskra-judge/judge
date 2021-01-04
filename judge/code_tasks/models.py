import markdown
from django.db import models

from judge.core import models as audit_models


class CodeSubmissionType(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class CodeTaskCategory(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Difficulty(models.Model):
    name = models.CharField(max_length=20)
    number_representation = models.IntegerField()

    def __str__(self):
        return f'{self.name} ({self.number_representation})'

    class Meta:
        verbose_name_plural = 'difficulties'


class CodeTask(audit_models.AuditModel):
    name = models.CharField(max_length=30)
    description_md = models.TextField()
    description_html = models.TextField(blank=True)
    description_preview = models.TextField(blank=True)

    code_submission_types = models.ManyToManyField(CodeSubmissionType)
    categories = models.ManyToManyField(CodeTaskCategory)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE)
    time_limit_in_ms = models.IntegerField(default=100)
    memory_limit_in_bytes = models.IntegerField(default=16)


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.description_html = markdown.markdown(self.description_md)
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    def __str__(self):
        return self.name


class TaskTest(audit_models.AuditModel):
    input = models.TextField()
    expected_output = models.TextField()
    code_task = models.ForeignKey(CodeTask, on_delete=models.CASCADE)
