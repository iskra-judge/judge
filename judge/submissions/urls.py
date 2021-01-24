from django.urls import path

from . import api_views, views

from .signals import *

urlpatterns = (
    path('submit/', api_views.CreateSubmissionApiView.as_view(), name='submit submission'),
    path('user/', api_views.UserSubmissionsApiView.as_view(), name='user submissions'),
    path('details/<int:pk>', views.SubmissionDetailsView.as_view(), name='submission details')
)
