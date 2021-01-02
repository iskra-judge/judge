import uuid
from tempfile import gettempdir
from os.path import join

from celery import shared_task
from django.apps import apps
from django.db import transaction

from judge.submissions.code_executors.cpp_docker_executor import CppDockerExecutor
from judge.submissions.code_executors.java_docker_executor import JavaDockerExecutor
from judge.submissions.code_executors.python_docker_executor import PythonDockerExecutor

@shared_task
@transaction.atomic()
def check_for_unprocessed_submission():
    Submission = apps.get_model(app_label='submissions', model_name='Submission')
    submissions_for_processing = Submission.objects.filter(processing_state=Submission.PROCESSING_STATE_NOT_STARTED)
    for submission in submissions_for_processing:
        submission.processing_state = Submission.PROCESSING_STATE_ENQUEUED_FOR_PROCESSING
        submission.save()

    for submission in submissions_for_processing:
        process_submission.delay(submission.id)


def get_executor(type):
    name_to_executor = {
        'python': PythonDockerExecutor(),
        'c++': CppDockerExecutor(),
        'java': JavaDockerExecutor(),
    }

    return name_to_executor[type.name.lower()]


@shared_task
def process_submission(submission_id):
    Submission = apps.get_model(app_label='submissions', model_name='Submission')
    submission = Submission.objects.filter(pk=submission_id).first()
    file_path = join(gettempdir(), f'submission-{uuid.uuid4()}.py')
    with open(file_path, 'w') as code_file:
        code_file.write(submission.code)

    executor = get_executor(submission.type)
    tests = [
        {
            'in': test.input,
            'out': test.expected_output,
        }
        for test in submission.code_task.tasktest_set.all()
    ]

    test_results = executor.execute(file_path, tests)
    [print(x) for x in test_results]
