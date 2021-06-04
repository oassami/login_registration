from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('user/register', views.user_register),
    path('user/login', views.user_login),
    path('success', views.user_seccess),
    path('clear_all', views.clear_forms),
]
