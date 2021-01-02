import time

from celery import shared_task


@shared_task(bind=True)
def do(self):
    time.sleep(100)
    print('It works!')
