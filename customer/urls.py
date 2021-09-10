from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from customer.views import *
from django.contrib.auth import views

app_name = 'customer'
urlpatterns = [
    # Template Views
    path('login/', MyLoginView.as_view(), name='login'),
    path('profile_detail/', ProfileView.as_view(), name='profile_detail'),
    path('logout/', auth_views.LogoutView.as_view(template_name='customer_temp/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('address_create/', AddressCreateView.as_view(), name='address_create'),
    path('update_info/<int:pk>', UpdateInfo.as_view(), name='update_info'),
    path('change_password/', MyPasswordChangeView.as_view(), name='change_password'),


   ]