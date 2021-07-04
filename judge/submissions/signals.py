from django.db.models.signals import post_save
from django.dispatch import receiver

from judge.submissions.models import Submission
from judge.submissions.tasks import process_submission, check_similar_submissions


@receiver(post_save, sender=Submission)
def judge_submission(sender, instance, created, **kwargs):
    print(instance.processing_state)
    if created:
        instance.processing_state = Submission.PROCESSING_STATE_ENQUEUED_FOR_JUDGING
        instance.save()
        process_submission.delay(instance.id)
    elif instance.processing_state == Submission.PROCESSING_STATE_JUDGED:
        print('Checking similarities')
        check_similar_submissions.delay(instance.id)
