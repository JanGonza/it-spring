from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Comment)
admin.site.register(models.Profile)
# admin.site.register(models.Lesson)


@admin.register(models.Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'material_type', 'publish')
    list_filter = ('created', 'updated', 'publish', 'material_type')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title', )}
    date_hierarchy = 'publish'
    ordering = ('material_type', 'publish')


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass

