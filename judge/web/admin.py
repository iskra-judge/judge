from django.contrib import admin

from judge.code_tasks.models import CodeSubmissionType, CodeTask, TaskTest
from judge.submissions.models import Submission, SubmissionTestResultType, SubmissionTestResult, SubmissionResult


class TaskTestInlineAdmin(admin.StackedInline):
    model = TaskTest


class CodeTaskAdmin(admin.ModelAdmin):
    inlines = (TaskTestInlineAdmin,)


admin.site.register(CodeSubmissionType)
admin.site.register(CodeTask, CodeTaskAdmin)
admin.site.register(Submission)
admin.site.register(SubmissionTestResultType)
admin.site.register(SubmissionTestResult)
admin.site.register(SubmissionResult)
