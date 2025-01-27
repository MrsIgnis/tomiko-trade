import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Cars, CarImage


class Command(BaseCommand):
    help = 'Сохранение всех изображений из media в БД'

    def handle(self, *args, **options):
        # Сбор всех доступных main изображений
        main_images = {}
        main_pattern = re.compile(r'main_(\d+)\.webp$')

        # Обработка main изображений
        for filename in os.listdir(settings.MEDIA_ROOT):
            if main_match := main_pattern.match(filename):
                car_number = int(main_match.group(1)) # Перехватываем эту группу чисел (\d+)
                main_images[car_number] = filename

        # Если нет main изображений - завершение работы
        if not main_images:
            self.stdout.write(self.style.ERROR('Изображения main не найдены!'))
            return

        # Получение отсортированного списка доступных номеров
        sorted_main_numbers = sorted(main_images.keys())
        total_main = len(sorted_main_numbers)

        # Распределение main изображения между машинами
        for car in Cars.objects.all():
            image_index = (car.id - 1) % total_main
            selected_number = sorted_main_numbers[image_index]
            filename = main_images[selected_number]

            # Создаем или обновляем запись
            CarImage.objects.get_or_create(
                car=car,
                image_type=CarImage.ImageType.MAIN,
                defaults={'image': filename}
            )
            self.stdout.write(f'Main: {filename} --> Car {car.id}')

        self.stdout.write(self.style.SUCCESS('Перенос изображений в БД завершён'))