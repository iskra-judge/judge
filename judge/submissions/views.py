from django.contrib.auth import mixins as auth_mixins
from django.views import generic as views

from judge.submissions.models import Submission


class UserSubmissionsView(auth_mixins.LoginRequiredMixin, views.ListView):
    template_name = 'submissions/user_submissions.html'

    def get_queryset(self):
        return Submission.objects.filter(user_id=self.request.user.id)


class SubmissionDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = Submission
    template_name = 'submissions/submission-details.html'

    def get_queryset(self):
        return Submission.objects.all().prefetch_related('submissionresult_set',
                                                         'submissionresult_set__submissiontestresult_set')

    def get_object(self, queryset=None):
        object = super().get_object(queryset)

        object.best_submission_result = object.submissionresult_set.order_by('-total_score').first()

        return object
