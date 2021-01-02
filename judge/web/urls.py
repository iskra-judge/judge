from django.urls import path

from judge.web.views import SubmissionView

urlpatterns = (
    path('submission/<int:task_pk>/', SubmissionView.as_view(), name='create submission'),
)