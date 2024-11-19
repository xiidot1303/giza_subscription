from django.apps import AppConfig


class payment(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'

    def ready(self):
        from payment.scheduled_job.updater import jobs
        jobs.scheduler.start()
