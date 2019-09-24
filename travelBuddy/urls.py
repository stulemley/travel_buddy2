"""travelBuddy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from travelBuddyApp import views

urlpatterns = [
    path('', views.index),
    path('main', views.main),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('travels', views.read_all_trips),
    path('travels/add', views.add_plan),
    path('create_trip', views.create_trip),
    path('destination/<int:num>', views.trip_info),
    path('join/<int:num>', views.join),
    path('admin/', admin.site.urls),
]
