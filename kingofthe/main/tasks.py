from django.utils import timezone as tz
from django.conf import settings

from celery import Celery

from . import models

app = Celery('tasks')
app.config_from_object(settings)

@app.task
def maybe_increment_hit(user_id):
    now = tz.now()
    delta = tz.timedelta(microseconds=settings.MINIMUM_CHECKIN_MICROSECONDS)
    if models.CheckinHit.objects.filter(user_id=user_id,
                                 created_at__gt=now - delta).exists():
        return

    models.CheckinHit.objects.create(user_id=user_id)
