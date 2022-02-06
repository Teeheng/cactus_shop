"""Cactus_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('item/', views.item, name='item'),
    path('about/', views.about, name='about-page'),
    path('contactus/', views.contactus, name='contactus'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('allproduct/', views.product, name='allproduct'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('addtocart/<int:pid>/', views.AddtoCart, name='addtocart'),
    path('mycart/', views.MyCart, name='MyCart'),
    path('mycart/edit', views.MyCartEdit, name='MyCartEdit'),
    path('checkout/', views.Checkout, name='checkout'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
