from celery import shared_task

from judge.submissions.services.code_similarity import CodeSimilarityService
from judge.submissions.services.submissions import SubmissionsService


@shared_task
def process_submission(submission_id, is_retest=False):
    SubmissionsService().judge_submission(submission_id, is_retest)
    if is_retest:
        return f'Submission#{submission_id} rejudged'
    else:
        return f'Submission#{submission_id} judged'


@shared_task
def check_similar_submissions(submission_id):
    CodeSimilarityService().check_similarity(submission_id)
