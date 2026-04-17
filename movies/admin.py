from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display  = ['title', 'genre', 'rating', 'created_at']
    list_filter   = ['genre']
    search_fields = ['title']