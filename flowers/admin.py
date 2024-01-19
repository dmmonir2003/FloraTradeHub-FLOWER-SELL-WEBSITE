from django.contrib import admin
from .models import FlowerCategories, Flower, OrderHistory

# Register your models here.

admin.site.register(FlowerCategories)
admin.site.register(Flower)
admin.site.register(OrderHistory)
