from django.urls import path

from . import views

urlpatterns = [
    path('', views.linguatec_home),
    path('search/', views.linguatec_search, name='search'),
]