"""banking_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from banking_app import views
from django.shortcuts import redirect


urlpatterns = [
   
    path('', views.home, name='home'), 
    path('admin_creation/', admin.site.urls),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('edit_customer/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('delete_customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    path('customer_login/', views.customer_login, name='customer_login'),
    path('customer_setup/', views.customer_setup, name='customer_setup'),
    path('customer_logout/', views.customer_logout, name='customer_logout'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('view_transactions/', views.view_transactions, name='view_transactions'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('download_transactions_pd/', views.download_transactions_pdf, name='download_transactions_pdf'),
    path('close_account/', views.close_account, name='close_account'),
    
]
