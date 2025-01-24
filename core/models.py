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
    engine_volume = models.CharField(max_length=250)
    drive = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    power_volume = models.CharField(max_length=250)
    brand_country = models.ForeignKey(Brands, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cars'

class CarPhoto(models.Model):
    car = models.ForeignKey(Cars, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/')
    is_main = models.BooleanField("Основное фото", default=False)

    def __str__(self):
        return f"{self.car} - {'Main' if self.is_main else 'Gallery'}"