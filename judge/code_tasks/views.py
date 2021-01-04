from django.contrib.auth import mixins as auth_mixins
from django.views import generic as views

from judge.code_tasks.models import CodeTask
from judge.submissions.models import Submission


class CodeTaskDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = CodeTask
    template_name = 'code_tasks/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code_task = self.get_object()
        context['submission_types'] = code_task.code_submission_types.all()
        user_submissions = list(Submission.objects \
                                .filter(user_id=self.request.user.id,
                                        code_task_id=code_task.id) \
                                .prefetch_related('submissionresult_set'))

        for submission in user_submissions:
            best_result = submission.submissionresult_set.order_by('-total_score').first()
            submission.total_score = best_result.total_score

        context['user_submissions'] = user_submissions

        return context
