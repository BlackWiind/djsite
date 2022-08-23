from django.contrib import admin

from .models import *


class WomanAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'contetnt')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_update')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Woman, WomanAdmin)
admin.site.register(Category, CategoryAdmin)
