from django.contrib.auth import mixins as auth_mixins
from django.views import generic as views

from judge.submissions.models import Submission


class UserSubmissionsView(auth_mixins.LoginRequiredMixin, views.ListView):
    template_name = 'submissions/user_submissions.html'

    def get_queryset(self):
        return Submission.objects.filter(user_id=self.request.user.id)
