from django.contrib.auth import get_user_model
from django.db import connection
from django.db.models import Max, Count
from django.views import generic as views

from judge.code_tasks.forms import CodeTaskFilterForm
from judge.code_tasks.models import CodeTask, CodeTaskCategory, Difficulty

UserModel = get_user_model()


class IndexView(views.ListView):
    template_name = 'index.html'
    context_object_name = 'code_tasks'
    selected_categories_ids = []
    selected_difficulties_ids = []

    def dispatch(self, request, *args, **kwargs):
        self.selected_categories_ids = self.request.GET.getlist('categories', [])
        self.selected_difficulties_ids = self.request.GET.getlist('difficulties', [])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filter_form'] = CodeTaskFilterForm(
            categories=CodeTaskCategory.objects.all(),
            difficulties=Difficulty.objects.all(),
            initial={
                'categories': self.selected_categories_ids,
                'difficulties': self.selected_difficulties_ids,
            }
        )

        return context

    def get_queryset(self):
        filter_obj = {}

        if self.selected_categories_ids:
            filter_obj['categories__id__in'] = self.selected_categories_ids
        if self.selected_difficulties_ids:
            filter_obj['difficulty_id__in'] = self.selected_difficulties_ids

        if self.selected_difficulties_ids or self.selected_categories_ids:
            queryset = CodeTask.objects.filter(**filter_obj)
        else:
            queryset = CodeTask.objects.all()
        return queryset.order_by('-date_created')


class UserRankingsView(views.ListView):
    model = UserModel
    template_name = 'submissions/user_rankings.html'
    context_object_name = 'users'

    def get_queryset(self):
        users = UserModel.objects.prefetch_related(
            'submission_set',
            'submission_set__submissionresult_set'
        )
        for user in users:
            submissions = user.submission_set.aggregate(code_task_id_c=Count('code_task_id'))
            print([f'{s}' for s in submissions])
            if submissions:
                user.submission_results = [self.__get_best_result(submission) for submission in submissions]
                if user.submission_results:
                    user.total_score = sum(
                        result['total_score__max'] for result in user.submission_results if result['total_score__max'])
                    user.problems_count = len(set(submission.code_task_id for submission in submissions))
                    user.submissions_count = len(submissions)
            else:
                user.total_score = 0
                user.problems_count = 0
                user.submissions_count = 0

        print(connection.queries)
        return sorted(users, key=lambda x: x.total_score, reverse=True)

    def __get_best_result(self, submission):
        return submission.submissionresult_set.all().aggregate(Max('total_score'))
