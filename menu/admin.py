from django.contrib import admin

from .models import Dish, OrderDish, Order,Customer

admin.site.register(Dish)
admin.site.register(OrderDish)
admin.site.register(Order)
admin.site.register(Customer)