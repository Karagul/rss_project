import os
from datetime import timedelta

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rss_project.settings')

app = Celery('rss_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

PREFIX_PATH = 'rss_project.applications.rss_reader.tasks.'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
# app.conf.update(
#     # task_annotations={
#     #     PREFIX_PATH+'read_currency': {'rate_limit': '1/s'}
#     # },
#     # task_routes={
#     #     PREFIX_PATH+'read_currency': {'queue': 'currency'},
#     #     PREFIX_PATH+'read_currencies': {'queue': 'currency'}
#     # },
#     beat_schedule={
#         'add-every-minute': {
#             'task': PREFIX_PATH+'read_currencies',
#             'schedule': timedelta(seconds=5),
#         }  # TODO it is not working
#     },
# )

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
