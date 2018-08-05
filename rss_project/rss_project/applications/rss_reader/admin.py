from django.contrib import admin

from .models import Currency

# Register your models here.


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['value', 'name', 'created']
    search_fields = list_display
