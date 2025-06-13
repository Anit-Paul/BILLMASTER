"""
URL configuration for BILLMASTER project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .views import operations
op=operations()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_product',op.add_product,name='add_product'),
    path('view_product',op.view_product,name='view_product'),
    path('delete_product',op.delete_product,name='delete_product'),
    path('delete',op.delete,name='delete'),
    path('get_bill',op.get_bill,name='get_bill'),
    path('save',op.save,name='save'),
    path('bill_page',op.bill_page,name='bill_page'),
    path('add_bill',op.add_bill,name='add_bill'),
    path('add_bill',op.add_bill,name='add_bill'),
    path('generate',op.generate,name='generate'),
    path('get_copy',op.get_copy,name='get_copy'),
    path('send_mail',op.send_mail,name='send_mail'),
    path('pre_send',op.pre_send,name='pre_send'),
]
