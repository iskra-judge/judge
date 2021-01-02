from django import forms
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from judge.submissions.models import Submission
from judge.code_tasks.models import CodeTask


class SubmissionForm(forms.Form):
    task_id = forms.CharField(widget=forms.HiddenInput())
    code = forms.CharField(widget=forms.Textarea())
    submission_type_id = forms.IntegerField()


class SubmissionView(TemplateView):
    template_name = 'submissions/create.html'

    def get_context_data(self, **kwargs):
        form = kwargs.pop('form', None)
        context = super().get_context_data(**kwargs)

        code_task = CodeTask.objects.filter(pk=self.kwargs['task_pk']).first()
        context['form'] = form or SubmissionForm(initial={'task_id': code_task.id})
        context['submission_types'] = code_task.code_submission_types.all()
        return context

    def post(self, request, task_pk):
        form = SubmissionForm(request.POST)
        if not form.is_valid():
            return render(self.template_name, self.get_context_data(form=form))

        data = form.cleaned_data
        task_id = data.pop('task_id')
        code = data.pop('code')
        submisstion_type_id = data.pop('submission_type_id')
        s = Submission(
            code_task_id=task_id,
            code=code,
            type_id=submisstion_type_id
        )

        s.save()
        return redirect('create submission', task_id)
