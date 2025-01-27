from django.contrib import admin
from .models import Brands, Cars, CarImage

@admin.register(Brands)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'country', 'brand']
    search_fields = ['id', 'country', 'brand']

@admin.register(Cars)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'year', 'mileage', 'price', 'transmission', 'engine_volume', 'drive', 'color']
    search_fields = ['id', 'model', 'year', 'mileage', 'price', 'transmission', 'engine_volume', 'drive', 'color']

@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_type', 'image', 'order']
    search_fields = ['id', 'image_type', 'image', 'order']