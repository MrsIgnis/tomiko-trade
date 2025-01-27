from django.db import models

class Brands(models.Model):
    country = models.CharField(max_length=250)
    brand = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'brands'


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