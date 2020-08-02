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
from django.shortcuts import redirect
# from django.http import HttpResponseRedirect

register = template.Library()

def email(request,table):
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
						'totalPrice': (int(cart[i]['quantity']) *dish.distPrice)

					}
			items.append(item)
		except:
			pass
		order['is_ordered'] = False

	context = {'items':items, 'order':order,'table': table}
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
	# print(post_pdf.pdf.read())
	# send_pdf = pdf(request)
	# print(send_pdf)
	# base_dir = 'media/documents/'
	# email.attach_file(send_pdf)
	email.attach('file.pdf', post_pdf, 'application/pdf')
	# email.send()
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
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart ={}
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
			items.append(item)
		except:
			pass
		order['is_ordered'] = False
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


def form(request):
	return render(request, "menu/form.html")

def saveDetails(request, customer):
	order = Order()
	order.customer = customer
	order.is_ordered = True
	order.save()

	cart = json.loads(request.COOKIES['cart'])
	for i in  cart:
		try:
			dish = Dish.objects.get(dishId=i)
			orderDish =  OrderDish.objects.create(order=order, dish=dish)
			orderDish.ordered = True
			orderDish.quantity = int(cart[i]['quantity'])
			orderDish.comments = cart[i]['dishComments']
			orderDish.save()
		except:
			pass




def formSubmit(request):

	if request.method == 'POST':
		name  = request.POST.get('cusName')
		phone  = request.POST.get('cusPhone')
		table = request.POST.get('cusTable')
		customer = Customer()
		tableNumber = request.POST['table']
		customer.table_number = request.POST['table']
		customer.name = request.POST['name']
		customer.phone = request.POST['phone']
		

		customer.save()
		saveDetails(request,customer)
		# print(customer)
		sendEmail = email(request, tableNumber)
		
		return sendEmail
		# create a form instance and populate it with data from the request:
		# check whether it's valid:
		# print(form)
		# if form.is_valid():
		# 	# process the data in form. as required
		# 	# redirect to a new URL:
		# 	return HttpResponseRedirect('/thanks/')
	# if a GET (or any other method) we'll create a blank form
	return HttpResponse('Order is placed')