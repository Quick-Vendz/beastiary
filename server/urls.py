# server urls
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='server_home'),
]