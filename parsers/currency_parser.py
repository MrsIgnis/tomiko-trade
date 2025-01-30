import requests
from decimal import Decimal
from core.models import Currency

def parser_currency_rates():
    """Функция парсинга курсов валют через GraphQL API."""

    URL = "https://bbr.ru/graphql/"

    HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    QUERY = """
        query RatesList($rateType: RateTypeEnum, $citySlug: String, $range: InputRateRange, $officeId: Int) {
          rates(
            noPagination: true
            rateType: $rateType
            citySlug: $citySlug
            officeId: $officeId
            range: $range
          ) {
            actualAt
            elements {
              id
              rateType
              fromCurrency {
                code
              }
              toCurrency {
                code
              }
              buyRate
              sellRate
              lot
            }
          }
        }
        """

    VARIABLES = {
        "rateType": "CASH_EXCHANGE",
        "citySlug": "vladivostok",
        "officeId": 7,
        "range": {"start": 0, "end": 10000}
    }

    response = requests.post(URL, json={"query": QUERY, "variables": VARIABLES}, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        elements = data.get("data", {}).get("rates", {}).get("elements", [])

        for item in elements:
            try:
                currency_code = item["fromCurrency"]["code"]
                buy_rate = Decimal(str(item["buyRate"])).quantize(Decimal('0.01'))
                sell_rate = Decimal(str(item["sellRate"])).quantize(Decimal('0.01'))

                # Пытаемся получить валюту из базы данных
                currency, created = Currency.objects.get_or_create(
                    code=currency_code,
                    defaults={'buy_rate': buy_rate, 'sell_rate': sell_rate}
                )

                # Если валюта не была создана, обновляем её значения
                if not created:
                    currency.buy_rate = buy_rate
                    currency.sell_rate = sell_rate
                    currency.save()

                print(f"{currency_code}: {buy_rate} / {sell_rate} {'(Создана)' if created else '(Обновлена)'}")

            except Exception as e:
                print(f"Ошибка при обработке {currency_code}: {e}")

    else:
        print(f"Ошибка запроса: {response.status_code}")