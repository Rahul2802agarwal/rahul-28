from django.contrib import admin

from .models import Dish, OrderDish, Order,Customer

class DishAdmin(admin.ModelAdmin):
	list_display =('dishId','dishName','dishDescription','distPrice','dishCategory')
	search_fields = ('dishName','distPrice','dishCategory')
	filter_horizontal = ()
	readonly_fields = ('dishId',)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ('Id','name','phone','table_number')
	search_fields = ('name','phone','table_number')
	filter_horizontal = ()
	readonly_fields = ('Id',)

class OrderAdmin(admin.ModelAdmin):
	list_display = ('id','customer','order_date','is_ordered')
class OrderDishAdmin(admin.ModelAdmin):
	list_display = ('id','ordered','dish','quantity','order','comments')
admin.site.register(Dish,DishAdmin)
admin.site.register(OrderDish,OrderDishAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Customer,CustomerAdmin)