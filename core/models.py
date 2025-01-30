from django.db import models

class Brands(models.Model):
    country = models.CharField(max_length=250)
    brand = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'brands'
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Cars(models.Model):
    model = models.CharField(max_length=250)
    year = models.IntegerField()
    mileage = models.IntegerField()
    price = models.IntegerField()
    transmission = models.CharField(max_length=20)
    engine_volume = models.IntegerField()
    drive = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    power_volume = models.CharField(max_length=250)
    brand_country = models.ForeignKey(Brands, models.DO_NOTHING, blank=True, null=True)
    car_images = models.ManyToManyField('CarImage', related_name='cars', blank=True)

    class Meta:
        managed = False
        db_table = 'cars'
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки авто'

    # Для удобства использования в html
    @property
    def main_image(self):
        return self.images.filter(image_type=CarImage.ImageType.MAIN).first()

    def gallery_images(self):
        return self.images.filter(image_type=CarImage.ImageType.GALLERY).order_by('order')


class CarImage(models.Model):
    class ImageType(models.TextChoices):
        MAIN = 'main', 'Main'
        GALLERY = 'gallery', 'Gallery'

    car = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='images')
    image_type = models.CharField(max_length=10, choices=ImageType.choices)
    image = models.ImageField(upload_to='')
    order = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'car_img'
        verbose_name = 'Изображение авто'
        verbose_name_plural = 'Изображения авто'


class Feedback(models.Model):
    name = models.CharField(max_length=25, verbose_name='Имя')
    phone_number = models.CharField(max_length=16, verbose_name='Телефон')
    message = models.TextField(max_length=200, blank=True, verbose_name='Сообщение')
    privacy_policy_confirm = models.BooleanField(default=False, verbose_name='С правилами политики конфиденциальности ознакомлен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        managed = True
        db_table = 'feedbacks'
        verbose_name = 'Пользовательская заявка'
        verbose_name_plural = 'Пользовательские заявки'