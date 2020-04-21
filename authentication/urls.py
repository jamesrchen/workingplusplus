from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginIndex, name='loginIndex'),
]

app_name = 'authentication'