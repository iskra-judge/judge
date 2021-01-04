from django.urls import path

from .api_views import CreateSubmissionApiView, UserSubmissionsApiView


from .signals import *

urlpatterns = (
    path('submit/', CreateSubmissionApiView.as_view(), name='submit submission'),
    path('user/', UserSubmissionsApiView.as_view(), name='user submissions'),
)
