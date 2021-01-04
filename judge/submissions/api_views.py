from rest_framework import generics as rest_views, permissions

from judge.submissions.models import Submission
from judge.submissions.serializers import ListSubmissionsSerializer, CreateSubmissionsSerializer


class CreateSubmissionApiView(rest_views.CreateAPIView):
    serializer_class = CreateSubmissionsSerializer
    queryset = Submission.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class UserSubmissionsApiView(rest_views.ListAPIView):
    serializer_class = ListSubmissionsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Submission.objects.filter(user_id=self.request.user.id)
