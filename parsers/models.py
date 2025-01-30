from django.db import models

class VKClip(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    preview_url = models.URLField(null=True, verbose_name='URL превью')
    post_url = models.URLField(verbose_name='URL поста')

    class Meta:
        managed = False
        verbose_name = 'Клип'
        verbose_name_plural = 'Клипы'

    def __str__(self):
        return self.title

class Review2GIS(models.Model):
    username = models.CharField(max_length=200, verbose_name='Имя пользователя')
    date = models.CharField(max_length=50, verbose_name='Дата')
    rating = models.IntegerField(choices=[(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')], verbose_name='Рейтинг')
    avatar = models.CharField(max_length=2, verbose_name='Аватарка')

    class Meta:
        managed = False
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"{self.username} - {self.rating} звезд"