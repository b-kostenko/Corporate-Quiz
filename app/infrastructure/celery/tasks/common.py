from app.infrastructure.celery.celery_app import celery_app


@celery_app.task(name="test_task")
def test_task() -> str:
    """
    A simple test task to verify Celery setup.
    """
    return "Celery is working!"
