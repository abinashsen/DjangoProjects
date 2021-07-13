from django.urls import path
from EcommerceApp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<pk>', views.customer, name='customer'),
    path('order/', views.order, name='order'),
    path('update_order/<pk>', views.update_order, name='update_order'),
    path('delete_order/<pk>', views.delete_order, name='delete_order'),
    path('add_product/', views.add_product, name='add_product'),
    path('update_product/<pk>', views.update_product, name='update_product'),
    path('delete_product/<pk>', views.delete_product, name='delete_product'),
    path('add_order/', views.add_order, name='add_order'),
    path('update_customer/<pk>', views.update_customer, name='update_customer'),
    path('delete_customer/<pk>', views.delete_customer, name='delete_customer'),
    path('register', views.registerpage, name='register'),
    path('login', views.loginpage, name='login'),
    path('logout', views.logoutpage, name='logout'),
    path('userpage', views.userpage, name='user-page'),
    path('account_settings', views.account_settings, name='account_settings'),

]
