from django.contrib import admin
from .models import VKClip, Review2GIS


@admin.register(VKClip)
class VKClipAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'preview_url', 'post_url']
    search_fields = ['title', 'description', 'preview_url', 'post_url']

@admin.register(Review2GIS)
class Review2GISAdmin(admin.ModelAdmin):
    list_display = ['avatar', 'username', 'date', 'rating']
    search_fields = ['avatar', 'username', 'date', 'rating']