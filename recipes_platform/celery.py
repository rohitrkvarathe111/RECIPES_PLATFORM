import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipes_platform.settings")

app = Celery("recipes_platform")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()



app.conf.beat_schedule = {
    'send-daily-email': {
        'task': 'recipes.tasks.send_daily_email',
        'schedule': crontab(hour=6, minute=0), 
    },
    'weekly-user-export': {
        'task': 'recipes.tasks.weekly_user_export_to_s3',
        'schedule': crontab(hour=2, minute=0, day_of_week='monday'),
    },
}
