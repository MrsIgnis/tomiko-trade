"""
URL configuration for webbin project.

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
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('actions/', views.actions, name='actions'),
    path('contacts/', views.contacts, name='contacts'),
    re_path(r'^(?P<country>korea|china|japan)/$', views.cars_catalog, name='cars_catalog'),
    re_path(r'^(?P<country>korea|china|japan)/get_models_by_brand/$', views.get_models_by_brand, name='get_models_by_brand'),
    #path('', views.empty, name='empty'),

    #path('', views.empty, name='empty'),

    re_path(r'^.*$', views.custom_page_not_found, {'exception': Exception('Not Found')}),
]
