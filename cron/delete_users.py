import logging
from django.conf import settings
from django.contrib.auth import get_user_model
logger = logging.getLogger('django')
User = get_user_model()

def f_delete_users():
    try:
        count = User.objects.filter(email_confirmat=False).delete()
        logger.info(f"Deleted {count[0]} unconfirmed users.")
    except Exception as e:
        logger.error(f"Error deleting unconfirmed users: {e}")