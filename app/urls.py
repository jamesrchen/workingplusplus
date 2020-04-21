from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.appIndex, name='appIndex'),
    path('dashboard/', views.appDashboard, name='appDashboard'),
    path('clockIn/', views.appClockIn, name="clockIn"),
    path('clockOut/', views.appClockOut, name="clockOut"),
]

app_name = 'app'