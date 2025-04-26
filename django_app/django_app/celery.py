import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app_settings')

app = Celery('django_app')

app.config_from_object('django.conf:settings' , namespace = 'Celery')

app.autodiscover_tasks()

app.conf.update(
    broker_url = 'redis://localhost:6379/0',
    result_backend = 'redis://localhost:6379/0',
)

@app.task(bind= True, ignore_result = True)
def debug_task(self):
    print(f'Request: {self.request!r}')