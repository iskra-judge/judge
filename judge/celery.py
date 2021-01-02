import os

from celery import Celery

from judge.submissions.tasks import check_for_unprocessed_submission

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'judge.settings')

app = Celery('judge')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, check_submissions.s())


@app.task
def check_submissions():
    check_for_unprocessed_submission.delay()