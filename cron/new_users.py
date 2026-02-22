import logging
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

logger = logging.getLogger('django')
User = get_user_model()

def f_new_users():
    try:
        recent_users = User.objects.filter(date_joined__gte = timezone.now() - timedelta(days = settings.Z2))
        for u in recent_users:
            logger.info(f"New user registered: {u.username}, joined at {u.date_joined}.")
    except Exception as e:
        logger.error(f"Error logging new users: {e}")