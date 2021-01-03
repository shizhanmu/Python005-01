from django.urls import path, include
from . import views

app_name = 'shortcomment'

urlpatterns = [
    path('', views.index, name='shortcomment-index'),
    path('search/', views.search, name='search'),
]