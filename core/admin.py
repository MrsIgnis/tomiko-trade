from django.contrib import admin
from .models import Brands, Cars, CarPhoto

@admin.register(Brands)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['country', 'brand']
    search_field = ['country', 'brand']

@admin.register(Cars)
class CarAdmin(admin.ModelAdmin):
    list_display = ['model', 'year', 'mileage', 'price', 'transmission', 'engine_volume', 'drive', 'color', 'power_volume']
    search_field = ['model', 'year', 'mileage', 'price', 'transmission', 'engine_volume', 'drive', 'color', 'power_volume']

'''class CarPhotoInline(admin.TabularInline):
    model = CarPhoto
    extra = 0  # Не показывать пустые поля
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        return f'<img src="{obj.image.url}" style="max-height: 100px;" />' if obj.image else ""

    image_preview.allow_tags = True
    image_preview.short_description = "Превью"

@admin.register(Cars)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year']
    inlines = [CarPhotoInline]

@admin.register(CarPhoto)
class CarPhotoAdmin(admin.ModelAdmin):
    list_display = ['car', 'is_main', 'image_tag']
    list_filter = ['is_main']
    readonly_fields = ['image_tag']'''