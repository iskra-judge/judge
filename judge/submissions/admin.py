from django.contrib import admin
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.html import format_html

from judge.submissions.models import Submission, SubmissionTestResult, SubmissionResult, SubmissionTestResultType
from judge.submissions.tasks import process_submission


class SubmissionResultInlineAdmin(admin.StackedInline):
    model = SubmissionResult
    readonly_fields = ('total_score', 'date_created')
    exclude = ('is_retest', )
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'processing_state', 'user', 'submission_type', 'total_score', 'code_task')
    inlines = (SubmissionResultInlineAdmin,)
    actions = ('rejudge',)
    sortable_by = ('submission_type', 'total_score', 'code_task', 'id')

    list_filter = ('user', 'code_task')


    def submission_type(self, obj):
        return obj.type.name

    def total_score(self, obj):
        return obj.submissionresult_set.aggregate(Max('total_score'))['total_score__max']

    def code_task(self, obj):
        return obj.code_task


class SubmissionTestResultInlineAdmin(admin.StackedInline):
    model = SubmissionTestResult

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


@admin.register(SubmissionResult)
class SubmissionResultAdmin(admin.ModelAdmin):
    inlines = (SubmissionTestResultInlineAdmin,)
    list_display = ('total_score', 'is_retest', 'go_to_submission')
    fields = ('go_to_submission', 'total_score')

    def has_change_permission(self, request, obj=None):
        return False

    def go_to_submission(self, obj):
        url = reverse_lazy('admin:submissions_submission_change', args=(obj.code_submission_id,))
        return format_html('<a href={}>{}', url, 'See submission')


@admin.register(SubmissionTestResultType)
class SubmissionTestResultTypeAdmin(admin.ModelAdmin):
    pass
