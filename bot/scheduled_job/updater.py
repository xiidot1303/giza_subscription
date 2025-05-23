from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from bot.scheduled_job import mailing
from asgiref.sync import async_to_sync

class jobs:
    scheduler = BackgroundScheduler(timezone='Asia/Tashkent')
    # scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    # register_events(scheduler)
    scheduler.add_job(mailing.send_message, 'interval', minutes=5)
    scheduler.add_job(async_to_sync(mailing.send_survey), 'cron', day=1, hour=15, minute=0)
