from django.core.management.base import BaseCommand
from parsers.currency_parser import parser_currency_rates

class Command(BaseCommand):
    help = 'Запускает парсер валют'

    def handle(self, *args, **options):
        parser_currency_rates()