import logging

from aiogram import Bot
from apscheduler.events import JobExecutionEvent
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler_di import ContextSchedulerDecorator
from rodi import Container

from bot.schedulers.exceptions import DeleteRequest
from bot.config import load_config
from bot.models.config import Config
from bot.models.config.main import Paths


async def handle_job_error(event: JobExecutionEvent, ctx: Container):
    logging.error(f'{event.exception=}')
    if isinstance(event.exception, DeleteRequest):
        scheduler = ctx.build_provider().get(BaseScheduler)
        scheduler.remove_job(event.job_id)


def setup_scheduler(bot=None, config: Config = None, paths: Paths = None):
    if not config:
        config = load_config(paths)

    job_stores = {
        "default": RedisJobStore(
            db=config.storage.redis.db,
            host=config.storage.redis.url,
            port=config.storage.redis.port,
            jobs_key="dispatched_trips_jobs", run_times_key="dispatched_trips_running"
        )
    }

    scheduler = ContextSchedulerDecorator(
        AsyncIOScheduler(jobstores=job_stores, timezone='Europe/Moscow')
    )
    if not bot:
        bot = Bot(config.bot.token)
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.ctx.add_instance(scheduler, declared_class=BaseScheduler)

    scheduler.on_job_error += handle_job_error
    return scheduler