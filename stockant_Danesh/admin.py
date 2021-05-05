from django.contrib import admin
from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(Stock)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']\



@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'stock', 'open', 'close', 'day_high', 'day_low', 'created', 'modified']


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'stock', 'current_price', 'target_price', 'horizon', 'period', 'number', 'year', 'accuracy']
