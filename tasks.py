from celery import Celery
from celery.utils.log import get_task_logger
import dribbble_util
import settings

celery = Celery(__name__, broker=settings.CELERY_BROKER_URL,
                backend=settings.CELERY_RESULT_BACKEND)
celery.config_from_object('settings')
logger = get_task_logger(__name__)


@celery.task(name="tasks.request", default_retry_delay=100, max_retries=3)
def request(url):
    d = dribbble_util.Dribbble()
    palette = d.shotPalette(url)
    if len(palette) == 0:
        print "retrying..."
        request.retry(args=[url], countdown=2)
    return palette
