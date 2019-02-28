import coreapi
import urllib.parse

from django.conf import settings
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.urls import resolve

from linguatec_lexicon_frontend import utils


class MenuItem(object):
    name = ''
    url = ''
    active = False

    def __init__(self, name, url, current_url=None):
        self.name = name
        self.url = url
        self.active = (self.url == current_url)


class LinguatecBaseView(TemplateView):

    def get_context_data(self, **kwargs):
        # detect active menu-item
        current_view = resolve(self.request.path_info)

        context = super().get_context_data(**kwargs)
        context['menu'] = self.generate_menu_items(current_view.url_name)
        context['menu_footer_lg'] = self.generate_menu_footer_lg_items()

        api_url = settings.LINGUATEC_LEXICON_API_URL
        client = coreapi.Client()
        schema = client.get(api_url)
        context['autocomplete_api_url'] = schema['words'] + 'near/'

        # Font Awesome Free or PRO
        if getattr(settings, 'LINGUATEC_FONTAWESOME_PRO', False):
            context['fa_class'] = 'fal'
        else:
            context['fa_class'] = 'fas'

        return context

    def generate_menu_items(self, current_url_name):
        urls = (
            (
                MenuItem('Inicio', 'home', current_url_name),
                MenuItem('Proyecto Linguatec', 'linguatec-project', current_url_name),
                MenuItem('Contacto', 'contact', current_url_name),
                MenuItem('Ayuda', 'help', current_url_name),
            ),
            (
                MenuItem('Aviso legal', 'legal-notice', current_url_name),
                MenuItem('Política de privacidad', 'privacy-policy', current_url_name),
            ),
        )

        return urls  # menu

    def generate_menu_footer_lg_items(self):
        urls = (
            MenuItem('Aviso legal', 'legal-notice'),
            MenuItem('Política de privacidad', 'privacy-policy'),
            MenuItem('Contacto', 'contact'),
            MenuItem('Ayuda', 'help'),
        )
        return urls


class HomeView(LinguatecBaseView):
    template_name = 'linguatec_lexicon_frontend/home.html'


class HelpView(LinguatecBaseView):
    template_name = 'linguatec_lexicon_frontend/help.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["gramcats"] = utils.retrieve_gramcats()
        return context


class ContactView(LinguatecBaseView):
    template_name = "linguatec_lexicon_frontend/contact.html"


class LegalNoticeView(LinguatecBaseView):
    template_name = "linguatec_lexicon_frontend/legal-notice.html"


class LinguatecProjectView(LinguatecBaseView):
    template_name = "linguatec_lexicon_frontend/linguatec-project.html"


class PrivacyPolicy(LinguatecBaseView):
    template_name = "linguatec_lexicon_frontend/privacy-policy.html"


class SearchView(LinguatecBaseView):
    template_name = "linguatec_lexicon_frontend/search_results.html"

    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        query = request.GET.get('q', None)
        if query is not None:
            api_url = settings.LINGUATEC_LEXICON_API_URL
            client = coreapi.Client()
            schema = client.get(api_url)
            querystring_args = {'q': query}
            url = schema['words'] + 'search/?' + \
                urllib.parse.urlencode(querystring_args)
            response = client.get(url)
            results = response["results"]
            context.update({
                'query': query,
                'results': results,
            })

            if response["count"] == 0:
                context["near_words"] = utils.retrieve_near_words(query)

        return TemplateResponse(request, 'linguatec_lexicon_frontend/search_results.html', context)


class WordDetailView(LinguatecBaseView):
    template_name = "linguatec_lexicon_frontend/search_results.html"

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        context = self.get_context_data(**kwargs)

        api_url = settings.LINGUATEC_LEXICON_API_URL
        client = coreapi.Client()
        schema = client.get(api_url)
        url = schema['words'] + '{pk}/'.format(pk=pk)
        word = client.get(url)

        context.update({
            'results': [word],
        })

        return TemplateResponse(request, self.template_name, context)
