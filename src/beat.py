import asyncio

from celery import Celery

from .config import RABBITMQ_DEFAULT_PASS, RABBITMQ_DEFAULT_USER
from .main import redis
from .menu.sheets_parser import get_rows
from .menu.tasks_utils import synchronize

RABBITMQ_DEFAULT_USER = RABBITMQ_DEFAULT_USER
RABBITMQ_DEFAULT_PASS = RABBITMQ_DEFAULT_PASS

celery = Celery('sync_data',
                broker=f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@rabbit:5672')


@celery.task
def synchronize_from_doc() -> None:
    values = get_rows()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(synchronize(values, redis))


celery.add_periodic_task(15.0, synchronize_from_doc.s(), name='sync every 15')
