from django.contrib import admin

from judge.submissions.models import SubmissionSimilarity


@admin.register(SubmissionSimilarity)
class SubmissionSimilarityAdmin(admin.ModelAdmin):
    list_display = ('task', 'user1', 'user2', 'jaccard_similarity', 'lcs_similarity', 'cosine_similarity')
    list_filter = ('jaccard_similarity', 'lcs_similarity', 'cosine_similarity')
    sortable_by = ('jaccard_similarity', 'lcs_similarity', 'cosine_similarity')

    def task(self, obj):
        return obj.submission1.code_task.name

    def user1(self, obj):
        return obj.submission1.user.username

    def user2(self, obj):
        return obj.submission2.user.username
