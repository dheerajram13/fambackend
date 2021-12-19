import os

from celery import Celery

# defining the django settings to celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube.settings')

app = Celery('youtube')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-youtube-data-every-10-secs':{
        'task':'search.tasks.retrieve_data',
        'schedule':30.0
    }
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')