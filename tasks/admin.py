from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_completed', 'created_at', 'updated_at')
    list_filter = ('title','user','is_completed', 'created_at')
    search_fields = ('title', 'description')
