from django.contrib import admin
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.html import format_html

from judge.submissions.models import Submission, SubmissionTestResult, SubmissionResult, SubmissionTestResultType
from judge.submissions.tasks import process_submission


class SubmissionResultInlineAdmin(admin.StackedInline):
    model = SubmissionResult
    readonly_fields = ('total_score', 'is_retest', 'date_created')
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False


class SubmissionAdmin(admin.ModelAdmin):
    inlines = (SubmissionResultInlineAdmin,)
    change_form_template = 'admin/submission_change_form.html'
    list_display = ('id', 'processing_state', 'user', 'submission_type', 'total_score')
    actions = ('rejudge',)

    list_filter = ('user',)

    def __rejudge(self, submissions):
        for submission in submissions:
            submission.processing_state = Submission.PROCESSING_STATE_ENQUEUED_FOR_JUDGING
            submission.save()
            process_submission.delay(submission.id, is_retest=True)

    def response_change(self, request, obj):
        if 'rejudge_submission' in request.POST:
            self.__rejudge([obj])
            return HttpResponseRedirect('.')
        return super().response_change(request, obj)

    def rejudge(self, request, obj):
        self.__rejudge(obj)
        return HttpResponseRedirect('.')

    def submission_type(self, obj):
        return obj.type.name

    def total_score(self, obj):
        return obj.submissionresult_set.aggregate(Max('total_score'))['total_score__max']


class SubmissionTestResultInlineAdmin(admin.StackedInline):
    model = SubmissionTestResult

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


class SubmissionResultAdmin(admin.ModelAdmin):
    inlines = (SubmissionTestResultInlineAdmin,)
    list_display = ('total_score', 'is_retest', 'go_to_submission')
    fields = ('go_to_submission', 'total_score', 'is_retest')

    def has_change_permission(self, request, obj=None):
        return False

    def go_to_submission(self, obj):
        url = reverse_lazy('admin:submissions_submission_change', args=(obj.code_submission_id,))
        return format_html('<a href={}>{}', url, 'See submission')


admin.site.register(Submission, SubmissionAdmin)
admin.site.register(SubmissionResult, SubmissionResultAdmin)
admin.site.register(SubmissionTestResultType)
