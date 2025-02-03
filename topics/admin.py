from django.contrib import admin
from .models import Class, Topic, Slide

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_obj')

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'order')
    ordering = ('topic', 'order')
