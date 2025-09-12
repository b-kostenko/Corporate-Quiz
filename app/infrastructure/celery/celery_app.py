from celery import Celery, Task

from app.settings import settings

celery_app: Celery = Celery(
    main="app",
    broker=settings.celery.celery_broker,
    backend=settings.celery.celery_backend,
    include=[
        "app.infrastructure.celery.tasks.common",
    ],
    task_cls=Task,
)

celery_app.conf.update(
    task_track_started=True,
    result_expires=3600,  # 1h expiration time for results
    result_backend_transport_options={"visibility_timeout": 3600},
)

celery_app.conf.beat_schedule = {
    # "name": {
    #     "task": "<name>",
    #     "schedule": crontab(hour=0, minute=0),  # every day at 00:00
    # }
}
