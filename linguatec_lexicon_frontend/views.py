import coreapi
import urllib.parse
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.urls import reverse, NoReverseMatch


class MenuItem(object):
    name = ''
    url = ''
    active = False

    def __init__(self, name=None, url=None, active=False):
        self.name = name
        try:
            self.url = reverse(url)
        except NoReverseMatch:
            self.url = '#TODO-%s' % url  # TODO


class LinguatecBaseView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = self.generate_menu_items()
        return context

    def generate_menu_items(self):
        urls = (
            (
                MenuItem('Inicio', 'home'),
                MenuItem('Proyecto Linguatec', 'linguatec-project'),
                MenuItem('Ayuda', 'help'),
                MenuItem('Contacto', 'contact'),
            ),
            (
                MenuItem('Aviso legal', 'legal-notice'),
                MenuItem('Política de privacidad', 'privacy-policy'),
                MenuItem('Dirección General de Política Lingüística', 'dgpl'),
            ),
        )
        # TODO mark item as active (using url name)

        return urls  # menu


class HomeView(LinguatecBaseView):
    template_name = 'linguatec_lexicon_frontend/home.html'


class ContactView(LinguatecBaseView):
    template_name = "linguatec_lexicon_frontend/contact.html"


class LegalNoticeView(LinguatecBaseView):
    template_name = "linguatec_lexicon_frontend/legal-notice.html"


class PrivacyPolicy(LinguatecBaseView):
    template_name = "linguatec_lexicon_frontend/privacy-policy.html"


class SearchView(LinguatecBaseView):
    template_name = "linguatec_lexicon_frontend/search_results.html"

    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        query = request.GET.get('q', None)
        if query is not None:
            client = coreapi.Client()
            schema = client.get('http://api.conectividadcolectiva.org/')
            querystring_args = {'search': query}
            url = schema['words'] + '?' + urllib.parse.urlencode(querystring_args)
            results = client.get(url)

            context.update({
                'query': query,
                'results': results,
            })

        return TemplateResponse(request, 'linguatec_lexicon_frontend/search_results.html', context)
