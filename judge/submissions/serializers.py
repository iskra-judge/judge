from rest_framework import serializers

from judge.submissions.models import Submission


class CreateSubmissionsSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    code = serializers.CharField()
    submission_type_id = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        task_id = self.validated_data['task_id']
        code = self.validated_data['code']
        submission_type_id = self.validated_data['submission_type_id']
        user = self.context['request'].user

        submission = Submission(
            code_task_id=task_id,
            code=code,
            type_id=submission_type_id,
            user=user,
        )

        submission.save()
        return {
            'task_id': task_id,
            'code': code,
            'submission_type_id': submission_type_id,
        }


class ListSubmissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
