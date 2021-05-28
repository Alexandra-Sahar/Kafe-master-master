"""kafe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from udachi.views import render_page_home, render_page_bluda_lv, ostavit_otziv, otziv, NewsDetailView, contacts, \
    bronirovanie

from cart.views import cart_detail, cart_add, cart_remove

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', render_page_home, name='home'),
                  path('bluda/<vid>/', render_page_bluda_lv, name='bluda_lv'),
                  path('otziv/', otziv, name='otziv'),
                  path('ostavit_otziv/', ostavit_otziv, name='ostavit_otziv'),
                  path('bludaveiw/<pk>/', NewsDetailView.as_view(), name='detail_view'),
                  path('cart_detail/<bluda_id>/', cart_detail, name='cart_detail'),
                  path('cart_add/<bluda_id>/', cart_add, name='cart_add'),
                  path('cart_remove/<bluda_id>/', cart_remove, name='cart_remove'),
                  path('contacts/', contacts, name='contacts'),
                  path('bronirovanie/', bronirovanie, name='bronirovanie'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
