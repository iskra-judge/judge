from django.contrib import admin

from judge.web.models import CodeSubmissionType, CodeTask, TaskTest, Submission, SubmissionTestResultType, \
    SubmissionTestResult, SubmissionResult


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
