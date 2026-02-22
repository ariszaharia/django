import logging
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger('django')

def check_stock():
    from magazin_app.models import Produs
    try:
        stock_low = Produs.objects.filter(stock_quantity__lt=10)
        for produs in stock_low:
            logger.warning(f"Low stock for product {produs.name}: {produs.stock_quantity} left.")
    except Exception as e:
        logger.error(f"Error checking stock levels: {e}")