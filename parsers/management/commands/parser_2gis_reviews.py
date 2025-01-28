from django.core.management.base import BaseCommand
from parsers.models import Review2GIS
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

class Command(BaseCommand):
    help = 'Парсит отзывы с 2GIS и сохраняет в БД'

    def add_arguments(self, parser):
        parser.add_argument(
            'url',
            type=str,
            help='URL страницы с отзывами 2GIS'
        )

    def handle(self, *args, **kwargs):
        url = kwargs['url']

        # Настройка Selenium WebDriver (Chrome)
        service = ChromeService(executable_path=ChromeDriverManager().install())

        # Инициализация драйвера
        driver = webdriver.Chrome(service=service)

        try:
            # Загрузка страницы
            driver.get(url)

            # Ожидание загрузки контейнеров отзывов
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "_o7qbud")))

            # Получение отрендеренного html
            render_html = driver.page_source
            soup = BeautifulSoup(render_html, 'html.parser')

            time.sleep(5)

            # Поиск контейнеров с отзывами
            reviews = soup.find_all('div', class_="_o7qbud")

            for review in reviews:
                # Парсинг необходимых данных
                username = review.find('span', class_='_16s5yj36').text.strip()

                date = review.find('div', class_='_139ll30').text.strip()
                if ',' in date: date = date.split(',')[0].strip()

                positive_rating = len(review.find('div', class_='_1fkin5c').find_all('span'))

                avatar_initials = review.find('div', class_='_1ixpok8')
                # Если нет картинки на аватарке
                if avatar_initials:
                    avatar = avatar_initials.text.strip()

                # Если есть картинка на аватарке
                else:
                    avatar_image = review.find('div', class_='_1dk5lq4')
                    if avatar_image:
                        avatar_style_attributes = avatar_image.get('style')
                        if avatar_style_attributes:
                            url_match = re.search(r'url\("([^"]+)"\)', avatar_style_attributes)
                            if url_match:
                                avatar = url_match.group(1)

                # Создание и сохранение объекта отзыва
                Review2GIS.objects.update_or_create(
                    username=username,
                    date=date,
                    defaults={
                        'rating': positive_rating,
                        'avatar': avatar
                    }
                )

                self.stdout.write(self.style.SUCCESS(f'Успешно сохранен/обновлен отзыв от {username}'))
                print("\n")

            self.stdout.write('Парсинг завершен!')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при парсинге: {str(e)}'))

        finally:
            driver.quit()