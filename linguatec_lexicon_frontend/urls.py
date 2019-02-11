from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', views.linguatec_home, name='home'),
    path('aviso-legal/', views.LegalNoticeView.as_view(), name='legal-notice'),
    path('contacto/', views.ContactView.as_view(), name='contact'),
    path('politica-de-privacidad/', views.PrivacyPolicy.as_view(), name='privacy-policy'),
    path('dgpl/', RedirectView.as_view(url='http://lenguasdearagon.org'), name='dgpl'),
    path('search/', views.linguatec_search, name='search'),
]
