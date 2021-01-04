from django.urls import path

from judge.web.views import IndexView, UserRankingsView

urlpatterns = (
    path('', IndexView.as_view(), name='index'),
    path('rankings/', UserRankingsView.as_view(), name='user rankings'),
)
