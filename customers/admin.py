from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)
    list_per_page = 30
