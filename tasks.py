from celery import Celery
from celery.utils.log import get_task_logger
import dribbble_util
import settings
import time
import random

celery = Celery(__name__, broker=settings.CELERY_BROKER_URL,
                backend=settings.CELERY_RESULT_BACKEND)
celery.config_from_object('settings')
logger = get_task_logger(__name__)


@celery.task(name="tasks.request", default_retry_delay=100, max_retries=4)
def request(url):
    time.sleep(random.uniform(1, 4))
    d = dribbble_util.Dribbble()
    palette = d.shotPalette(url)
    return palette
