from celery import Celery, Task, shared_task
from celery.schedules import crontab
from . import models
from .mail import sendMail
from datetime import datetime, timedelta
from .packages import db


# making celery app in flask application context
def create_celery_app(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
               return self.run(*args, **kwargs)

    celery_app = Celery(app.name,broker="redis://127.0.0.1:6379/1", backend="redis://127.0.0.1:6379/2",task_cls=FlaskTask,broker_connection_retry_on_startup=True, timezone = 'Asia/Kolkata')
    
    celery_app.conf.beat_schedule = {
        'send-monthly-music-rating-report': {
            'task': 'Scheduled Job',
            # 'schedule': crontab(day_of_month=1, hour=18, minute=0),
            'schedule': 240,
        },

        'daily-reminder': {
            'task': 'Daily Reminder',
            # 'schedule': crontab(hour=18, minute=0),
            'schedule': 300,
        },
    }

    celery_app.set_default()
    return celery_app

# CORE Reminder job to send reminder to the users for the visting app
@shared_task(name="Daily Reminder")
def send_daily_remainder_emails():
    try:
        
        inactivity_threshold = datetime.utcnow() - timedelta(days=1)
        inactive_user = db.session.query(models.User).filter(models.User.role=='user').filter(models.User.last_login >= inactivity_threshold).all()

        # print(inactive_user)

        # Send reminder emails
        for user in inactive_user:
            subject = "Daily Listening Reminder & Today Updates"
            message = f"Dear {user.name}, you haven't visited the app today. Don't miss todays trending music!"
            sendMail(user.email, subject, message)

        return True
    except Exception as e:
        print(e)
        return False



# CORE scheduled job to send monthly report to the creator telling them about their rating on their uploaded songs
@shared_task(name="Scheduled Job")
def setup_periodic_tasks():
    
    users = models.User.query.filter_by(role = 'creator').all()
    
    for user in users:
        res = monthly_report(user.user_id, user.email)
        

    if(res): return [True,'Successfully Exported Monthly Report']
    else : return [False,'Failed to export monthly report']





def monthly_report(user_id, user_email):
    try:

        creator_report = db.session.query(models.User).filter_by(user_id=user_id).all()
        print(creator_report)

        # Send the email to user
        res = sendMail(user_email, "Monthly Report", "The monthly report of your bookings is attached below.", creator_report = creator_report)
        return res

    except Exception as e:
        print(e)
        return False