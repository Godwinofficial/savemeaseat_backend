from django.apps import AppConfig

def send_reminders_job():
    # This function is now in core/scheduler_jobs.py
    pass

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from apscheduler.schedulers.background import BackgroundScheduler
        from django_apscheduler.jobstores import DjangoJobStore
        from core.scheduler_jobs import send_reminders_job
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            send_reminders_job,
            'cron',
            hour=8,
            minute=0,
            id='send_reminders_job',
            replace_existing=True
        )
        scheduler.start()
