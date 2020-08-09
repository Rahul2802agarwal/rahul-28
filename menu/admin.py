from django.contrib import admin

from .models import Dish, OrderDish, Order,Customer

class DishAdmin(admin.ModelAdmin):
	list_display =('dishId','dishName','dishDescription','distPrice','dishCategory')
	search_fields = ('dishName','distPrice','dishCategory')
	filter_horizontal = ()
	readonly_fields = ('dishId',)
	empty_value_display = '-empty-'

class CustomerAdmin(admin.ModelAdmin):
	list_display = ('Id','name','phone','table_number')
	search_fields = ('name','phone','table_number')
	filter_horizontal = ()
	readonly_fields = ('Id',)
	empty_value_display = '-empty-'

class OrderAdmin(admin.ModelAdmin):
	list_display = ('id','customer','order_date','is_ordered','customer_name')
	list_filter = ('order_date',)
	search_fields = ('customer__Id',)
	filter_horizontal = ()
	readonly_fields = ('id',)
	empty_value_display = '-empty-'

	def customer_name(self, obj):
		return obj.customer.name

class OrderDishAdmin(admin.ModelAdmin):
	list_display = ('id','ordered','dish','quantity','order','comments')
	search_fields = ('order','quantity','dish')
	filter_horizontal = ()
	readonly_fields = ('id',)
	empty_value_display = '-empty-'

admin.site.register(Dish,DishAdmin)
admin.site.register(OrderDish,OrderDishAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Customer,CustomerAdmin)