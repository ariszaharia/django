import schedule
import time
import logging
import os
import django
import sys
from datetime import timedelta
from django.utils import timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magazin_fitness.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail

#date settings
from django.contrib.auth import get_user_model
logger = logging.getLogger('django')
User = get_user_model()
K = settings.K
Z = settings.Z
O = settings.O
X_MINUTES = settings.X_MINUTES


#functii cron
def f():
    try:
        count = User.objects.filter(email_confirmat=False).delete()
        logger.info(f"Deleted {count[0]} unconfirmed users.")
    except Exception as e:
        logger.error(f"Error deleting unconfirmed users: {e}")

def send_newsletter():
    try:
        utilizatori = User.objects.filter(date_joined__lte=timezone.now() - timedelta(minutes=X_MINUTES))
        utilizatori = utilizatori.filter(email_confirmat=True)
        for u in utilizatori: 
            send_mail(
                subject="Newsletter",
                message="This is a newsletter.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[u.email],
            )
            logger.info(f"Sent newsletter to {u.email}.")

    except Exception as e:
        logger.error(f"Error sending newsletters: {e}")

def check_stock():
    from magazin_app.models import Produs
    try:
        stock_low = Produs.objects.filter(stock_quantity__lt=10)
        for produs in stock_low:
            logger.warning(f"Low stock for product {produs.name}: {produs.stock_quantity} left.")
    except Exception as e:
        logger.error(f"Error checking stock levels: {e}")

def new_users():
    try:
        recent_users = User.objects.filter(date_joined__gte = timezone.now() - timedelta(days = settings.Z2))
        for u in recent_users:
            logger.info(f"New user registered: {u.username}, joined at {u.date_joined}.")
    except Exception as e:
        logger.error(f"Error logging new users: {e}")

schedule.every(K).minutes.do(f)
planficator_marti = getattr(schedule.every(), Z)
planficator_marti.at(O).do(send_newsletter)
logger.warning(f"Cron job started: Deleting unconfirmed users every {settings.K} minutes.")

while True:
    schedule.run_pending()
    time.sleep(1)