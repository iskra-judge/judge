from django.urls import path

from judge.code_tasks.views import CodeTaskDetailsView

urlpatterns = (
    path('<int:pk>/', CodeTaskDetailsView.as_view(), name='code task details'),
)
