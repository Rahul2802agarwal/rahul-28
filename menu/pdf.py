from django.http import JsonResponse
import json
from menu.utils import render_to_pdf
def pdf(request):
	cart = json.loads(request.COOKIES['cart'])
	items = []
	order = {'get_cart_total':0,'get_cart_items':0,'is_ordered':False}
	cartItems = []
	print('cart length:',len(cart))
	for i in cart:
		print(i)
		# cartItems += cart[i]['quantity']
		try:
			print(cart[i]['dishComments'])
			dish = Dish.objects.get(dishId=i)

			
			total =  (dish.distPrice * int(cart[i]['quantity']))
			order['get_cart_total'] += total
			order['get_cart_items'] += int(cart[i]['quantity'])

			item = {
						'dish':{
							'dishId':dish.dishId,
							'dishName':dish.dishName,
							'dishDescription':dish.dishDescription,
							'distPrice':dish.distPrice,
							'dishCategory':dish.dishCategory,
							'dishImage':dish.dishImage
						},
						'quantity':int(cart[i]['quantity']),
						'comments':cart[i]['dishComments']

					}
			items.append(item)
		except:
			pass
		order['is_ordered'] = False

	context = {'items':items, 'order':order}
	pdf = render_to_pdf('menu/invoice.html', context)
	return pdf