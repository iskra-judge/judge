from django.db import models


class AuditModel(models.Model):
    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    date_edited = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True
