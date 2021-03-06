from django.urls import path
from django.contrib import admin
from . import views


admin.site.site_header = 'Admin Panel'
admin.site.site_title  = 'admin title'
admin.site.index_title = 'admin index title'

urlpatterns = [
	#Leave as empty string for base url
	path('', views.menu, name="menu"),
	path('cart/', views.cart, name='cart'),
	path('update_item/', views.updateItem, name='updateItem'),
	# path('Pdf/', views.Pdfview, name='pdf')
	path('invoice/',views.GeneratePdf,name='GeneratePdf'),
	# path(r'^email/(?P<table>\d+)/$', views.email, name='email'),
	path('form/', views.form, name='form'),
	path('formSubmit/', views.formSubmit, name='formSubmit')
	# path('cart/', views.cart, name="cart"),
	# path('checkout/', views.checkout, name="checkout"),

]