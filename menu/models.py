from django.db import models

from django.contrib.auth.models import User


class Customer(models.Model):
    # phone = models.IntegerField()
    Id = models.AutoField(primary_key=True)
    table_number = models.IntegerField()

    def __str__(self):
        return str(self.table_number)


class Dish(models.Model):
	dishId = models.AutoField(primary_key=True)
	dishName = models.CharField(max_length=50)
	dishDescription = models.TextField()
	distPrice = models.FloatField()
	dishCategory = models.CharField(max_length=50)
	dishImage = models.ImageField()

	def __str__(self):
	    return self.dishName
	    
	@property
	def imageURL(self):
		try:
			url = self.dishImage.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	
	order_date = models.DateTimeField(auto_now_add=True)
	is_ordered = models.BooleanField(default=False)

	def __str__(self):
	    return '{0} - {1}'.format(self.customer.Id, self.customer.table_number)
	@property
	def get_cart_total(self):
		orderedItems = self.orderdish_set.all()
		
		total =  0
		for item in orderedItems:
			total += item.get_total_price()
		return total
	@property
	def get_cart_items(self):
		orderedItems = self.orderdish_set.all()
		total = sum([item.quantity for item in orderedItems])
		return total
	

class OrderDish(models.Model):
    ordered = models.BooleanField(default=False)
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.quantity} of {self.dish.dishName}"

    def get_total_price(self):
    	print('get the total price')
    	print('\n')
    	total = self.quantity * self.dish.distPrice
    	return total



