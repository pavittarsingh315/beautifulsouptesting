from django.urls import path

from . import views
from .views import SearchList

urlpatterns = [
    path('', views.home, name='index'),
    path('search/', views.new_search, name='search'),
    path('class/', SearchList.as_view(), name='hahaha')
]