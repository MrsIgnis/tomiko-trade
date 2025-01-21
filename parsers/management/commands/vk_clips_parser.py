from django.core.management.base import BaseCommand
from django.conf import settings
from parsers.models import VKClip
import vk_api

class Command(BaseCommand):
    help = 'Парсит клипы VK из указанного сообщества и добавляет (или обновляет) их в БД'


    def add_arguments(self, parser):
        parser.add_argument(
            '--group_id',
            type=str,
        )
        parser.add_argument(
            '--count',
            type=int,
            default=40,
        )


    def handle(self, *args, **options):
        try:
            # Получаем значения из настроек или аргументов команды
            group_id = options['group_id'] or getattr(settings, 'VK_GROUP_ID', None)
            access_token = getattr(settings, 'VK_ACCESS_TOKEN', None)
            count = options['count']

            if not group_id or not access_token:
                raise ValueError("Не указан GROUP_ID или ACCESS_TOKEN")

            # Инициализация VK API
            vk_session = vk_api.VkApi(token=access_token)
            vk = vk_session.get_api()

            self.stdout.write(f"Начинаем парсинг клипов из группы ID{group_id}...")

            # Получаем посты
            posts = vk.wall.get(owner_id=f"-{group_id}", count=count)

            clips_added = 0
            clips_updated = 0

            for post in posts['items']:
                if 'attachments' in post:
                    for attachment in post['attachments']:
                        if attachment['type'] == 'video':
                            video = attachment['video']

                            # Подготовка данных для создания/обновления
                            clip_data = {
                                'title': video.get('title', 'Без названия'),
                                'description': video.get('description', ''),
                                'preview_url': video.get('photo_1280'),
                                'post_url': f"https://vk.com/wall-{group_id}_{post['id']}"
                            }

                            # Создаем или обновляем запись в базе
                            clip, created = VKClip.objects.update_or_create(
                                post_url=clip_data['post_url'],
                                defaults=clip_data
                            )

                            if created:
                                clips_added += 1
                            else:
                                clips_updated += 1

            self.stdout.write(f'Парсинг завершен! Добавлено: {clips_added}, Обновлено: {clips_updated} клипов')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при парсинге: {str(e)}'))