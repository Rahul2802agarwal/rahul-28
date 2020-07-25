from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import View
import json
from django.conf import settings
# from django.contrib.auth.decorators import login_required
from .models import Dish, OrderDish, Order,Customer
from menu.utils import render_to_pdf
from menu.pdf import pdf
from django import template
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from django.core.mail import EmailMessage

register = template.Library()

def email(request):
	cart = json.loads(request.COOKIES['cart'])
	items = []
	order = {'get_cart_total':0,'get_cart_items':0,'is_ordered':False}
	cartItems = []
	for i in cart:
		try:
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
						'comments':cart[i]['dishComments'],
						'table_number': cart['table_number'],
						'totalPrice': (int(cart[i]['quantity']) *dish.distPrice)

					}
			items.append(item)
		except:
			pass
		order['is_ordered'] = False

	context = {'items':items, 'order':order,'table':cart['table_number']}
	email = 'aggarwal1997rahul@gmail.com'
	# email = 'siddharth16sharma@gmail.com'
	subject = 'Order Detail'
	message = 'Order detail of a customer'
	document = ''
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [email]
	email = EmailMessage(subject,message,email_from,recipient_list)
	post_pdf = render_to_pdf('menu/invoice.html',context)
	pdfData = HttpResponse(post_pdf, content_type='application/pdf')
	print(pdfData)
	print(type(pdfData))
	# print(post_pdf.pdf.read())
	# send_pdf = pdf(request)
	# print(send_pdf)
	# base_dir = 'media/documents/'
	# email.attach_file(send_pdf)
	email.attach('file.pdf', post_pdf, 'application/pdf')
	print(type(post_pdf))
	print('--------------------------------')
	email.send()
	# return HttpResponse('Order is placed')
	return pdfData

def GeneratePdf(request):
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
	return HttpResponse(pdf, content_type='application/pdf')


def menu(request):
	dishCategoriesList = list()
	dishs = Dish.objects.all()
	dishDetailCategorywise = dict()

	dishCategories = Dish.objects.order_by('dishCategory').values('dishCategory').distinct()
	for category in dishCategories:
		dishCategoriesList.append(category['dishCategory'])
		filterData =  Dish.objects.filter(dishCategory=category['dishCategory'])
		dishDetailCategorywise[category['dishCategory']] = filterData

	context = {
    'dishs': dishDetailCategorywise,
    'dishCategory': dishCategoriesList
	}
	# print(context)
	print(context)
	return render(request, "menu/dish.html", context)

def cart(request):
	# # customer = request.user.name
	# order,created =  Order.objects.get_or_create( is_ordered=False)
	# items = order.orderdish_set.all()
	
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart ={}
	# print('cart:',cart)
	items = []
	order = {'get_cart_total':0,'get_cart_items':0,'is_ordered':False}
	cartItems = []
	print('cart length:',len(cart))
	for i in cart:
		print(i)
		# cartItems += cart[i]['quantity']
		try:
			print(cart[i])
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
						'quantity':int(cart[i]['quantity'])

					}
			print('----------------------------------')
			print(item)
			print('------end----------------------')
			items.append(item)
		except:
			pass
		order['is_ordered'] = False
		# print('----------------------------------')
		# print(items)
		# print('------end----------------------')
	context = {'items':items, 'order':order}
	return render(request, "menu/cart.html", context)
		
	# order = 


def updateItem(request):
	data = json.loads(request.body)
	dishId = data['dishId']
	action =  data['action']
	dishQuantity = data['dishQuantity']
	dishComments = data['dishComments']

	dish, created = Dish.objects.get_or_create(dishId=dishId)
	order, created =  Order.objects.get_or_create( is_ordered=False)
	orderDish, created =  OrderDish.objects.get_or_create(order=order, dish=dish)


	if action == 'add':
		orderDish.quantity = dishQuantity
		orderDish.comments =  dishComments
	elif action == 'remove':
		orderDish.quantity -= 1

	orderDish.save()
	# if orderDish.quantity <= 0:
	# 	orderDish.delete()

	print(dishId, action, dishComments, dishQuantity)
	return JsonResponse('Item was added', safe=False)


