from django.contrib import admin

from .models import Robot


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = ('serial', 'created')
    search_fields = ('serial',)
    list_filter = ('model',)
    list_per_page = 30
