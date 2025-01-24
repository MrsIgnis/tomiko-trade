from django.db import models

class VKClip(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    preview_url = models.URLField(null=True, verbose_name='URL превью')
    post_url = models.URLField(verbose_name='URL поста')

    class Meta:
        verbose_name = 'Клип'
        verbose_name_plural = 'Клипы'

    def __str__(self):
        return self.title