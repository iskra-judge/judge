from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('judge.web.urls')),
    path('submissions/', include('judge.submissions.urls')),
    path('code-tasks/', include('judge.code_tasks.urls')),
    path('auth/', include('judge.judge_auth.urls')),
]
