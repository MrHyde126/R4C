from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'robot_serial')
    search_fields = ('customer__email', 'robot_serial')
    list_filter = ('customer',)
    list_per_page = 30
