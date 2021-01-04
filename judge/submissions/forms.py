from django import forms


class SubmissionForm(forms.Form):
    task_id = forms.CharField(widget=forms.HiddenInput())
    code = forms.CharField(widget=forms.Textarea())
    submission_type_id = forms.IntegerField()
