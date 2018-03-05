# -*- coding: utf-8 -*-

from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('mastermind/', include('mastermind.urls')),
    path('admin/', admin.site.urls),
]
