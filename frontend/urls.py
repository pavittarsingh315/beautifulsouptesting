from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('search/', views.new_search, name='search')
]