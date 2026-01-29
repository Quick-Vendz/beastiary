# client urls
from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:book_slug>/<slug:chapter_slug>/<slug:page_slug>/', views.page_view, name='page_with_chapter'),
    path('<slug:book_slug>/<slug:page_slug>/', views.page_view, name='page'),
]