from django.urls import path

from . import views

urlpatterns = [
    path('', views.linguatec_home),
    path('aviso-legal/', views.LegalNoticeView.as_view()),
    path('search/', views.linguatec_search, name='search'),
]
