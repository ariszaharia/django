import logging
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

logger = logging.getLogger('django')
User = get_user_model()
X_MINUTES = settings.X_MINUTES

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