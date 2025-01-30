from celery import shared_task
from .currency_parser import parser_currency_rates

@shared_task
def update_currency_rates():
    parser_currency_rates()
    return None