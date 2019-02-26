from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('aviso-legal/', views.LegalNoticeView.as_view(), name='legal-notice'),
    path('contacto/', views.ContactView.as_view(), name='contact'),
    path('politica-de-privacidad/', views.PrivacyPolicy.as_view(), name='privacy-policy'),
    path('proyect-linguatec/', views.LinguatecProjectView.as_view(), name='linguatec-project'),
    path('dgpl/', RedirectView.as_view(url='http://lenguasdearagon.org'), name='dgpl'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('words/<int:pk>/', views.WordDetailView.as_view(), name='word-detail')
]
