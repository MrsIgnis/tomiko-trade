from django.contrib import admin
from .models import VKClip

@admin.register(VKClip)
class ClipAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'preview_url', 'post_url']
    search_fields = ['title', 'description', 'preview_url', 'post_url']