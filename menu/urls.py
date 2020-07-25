from django.urls import path
from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.menu, name="menu"),
	path('cart/', views.cart, name='cart'),
	path('update_item/', views.updateItem, name='updateItem'),
	# path('Pdf/', views.Pdfview, name='pdf')
	path('invoice/',views.GeneratePdf,name='GeneratePdf'),
	path('email/', views.email, name='email'),
	# path('cart/', views.cart, name="cart"),
	# path('checkout/', views.checkout, name="checkout"),

]