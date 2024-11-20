from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from payment.scheduled_job import atmos_job
from asgiref.sync import async_to_sync


class jobs:
    scheduler = BackgroundScheduler(timezone='Asia/Tashkent')
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    scheduler.add_job(async_to_sync(
        atmos_job.update_access_token), 'interval', minutes=45)
