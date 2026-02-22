import os
import sys
import django
import time
import schedule
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magazin_fitness.settings')
django.setup()

from delete_users import f_delete_users
from send_newsletter import send_newsletter
from check_stock import check_stock
from new_users import f_new_users
from django.conf import settings

logger = logging.getLogger('django')

schedule.every(settings.K).minutes.do(f_delete_users)
schedule.every(settings.M).minutes.do(check_stock)

getattr(schedule.every(), settings.Z.lower()).at(settings.O).do(send_newsletter)

getattr(schedule.every(), settings.Z2.lower()).at(settings.O2).do(f_new_users)


logger.warning("Cron jobs scheduled.")

while True:
    schedule.run_pending()
    time.sleep(1)