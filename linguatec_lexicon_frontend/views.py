"""
The views.
"""
import urllib.parse
from collections import OrderedDict

from django.conf import settings
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.urls import resolve, reverse

import coreapi
from linguatec_lexicon_frontend import utils


def order_lexicons(src_languages, lexicons):
    res=[]
    count=0
    for source_language in src_languages:
        res.append([])
        for lex in lexicons:
            if source_language == lex.get('src_language'):
                res[count].append(lex)
        count=+1
    return res

def get_source_languages(lexicons):
    src_languages = []
    for lexicon in lexicons:
        if lexicon.get('src_language') not in src_languages:
            src_languages.append(lexicon.get('src_language'))
    return src_languages

class MenuItem(object):
    """Define a item of the website menu."""
    name = ''
    url = ''
    active = False

    def __init__(self, name, url, current_url=None):
        self.name = name
        self.url = url
        self.active = (self.url == current_url)


class LinguatecBaseView(TemplateView):
    """
    Base view that initializes the common context and
    the menu items of the website.
    """

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
        """Generate main menu navbar items."""
        urls = (
            (
                MenuItem('Inicio', 'home', current_url_name),
                MenuItem('Proyecto Linguatec',
                         'linguatec-project', current_url_name),
                MenuItem('Contacto', 'contact', current_url_name),
                MenuItem('Ayuda', 'help', current_url_name),
            ),
            (
                MenuItem('Aviso legal', 'legal-notice', current_url_name),
                MenuItem('Política de privacidad',
                         'privacy-policy', current_url_name),
            ),
        )

        return urls  # menu

    def generate_menu_footer_lg_items(self):
        """Generate footer menu used on lg+ devices."""
        urls = (
            MenuItem('Aviso legal', 'legal-notice'),
            MenuItem('Política de privacidad', 'privacy-policy'),
            MenuItem('Contacto', 'contact'),
            MenuItem('Ayuda', 'help'),
        )
        return urls

    def groupby_word_entries(self, word):
        """Group entries by variation.region"""
        common = []
        variations = OrderedDict()
        for entry in word['entries']:
            if entry['variation'] is None:
                common.append(entry)
            else:
                region = entry['variation']['region']
                if region not in variations:
                    variations[region] = []
                # TODO if we want to include gramcats may be inline
                # entry['gramcats_inline'] = ' / '.join([x['abbreviation'] for x in entry['gramcats']])
                variations[region].append(entry)
        word['entries_common'] = common
        word['entries_variations'] = variations

    def get_urls(self, word):
        """Get the urls in admin panel of word entries"""

        for entry in word['entries_common']:
            entry['url'] = reverse('admin:linguatec_lexicon_entry_change', args=(entry['id'],))

        for region, entry_list in word['entries_variations'].items():
            for entry in entry_list:
                entry['url'] = reverse('admin:linguatec_lexicon_entry_change', args=(entry['id'],))


class HomeView(LinguatecBaseView):
    template_name = 'linguatec_lexicon_frontend/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # show or not splash screen
        context["first_load"] = self.request.session.get('first_load', True)
        self.request.session['first_load'] = False

        api_url = settings.LINGUATEC_LEXICON_API_URL
        client = coreapi.Client()
        schema = client.get(api_url)
        url = schema['lexicons']
        response = client.get(url)
        lexicons = response["results"]

        src_languages = get_source_languages(lexicons)

        lexicons = order_lexicons(src_languages, lexicons)

        context.update({
            'lexicons': lexicons,
        })

        return context


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
        """Search and show results. If none, show near words."""
        context = self.get_context_data(**kwargs)
        query = request.GET.get('q', None)
        lex_code = request.GET.get('l', '')
        if query is not None:
            api_url = settings.LINGUATEC_LEXICON_API_URL
            client = coreapi.Client()
            schema = client.get(api_url)

            url = schema['lexicons']
            response = client.get(url)
            lexicons = response["results"]

            src_languages = get_source_languages(lexicons)

            lexicons = order_lexicons(src_languages, lexicons)

            querystring_args = {'q': query, 'l': lex_code}
            url = schema['words'] + 'search/?' + \
                urllib.parse.urlencode(querystring_args)
            response = client.get(url)
            results = response["results"]

            if response["count"] == 0:

                context.update({
                    'query': query,
                    'selected_lexicon': lex_code,
                    'lexicons': lexicons,
                })

                context["near_words"] = utils.retrieve_near_words(query, lex_code)

            else:
                for word in results:
                    self.groupby_word_entries(word)
                    self.get_urls(word)

                context.update({
                    'query': query,
                    'results': results,
                    'selected_lexicon': lex_code,
                    'lexicons': lexicons,
                })

        return TemplateResponse(request, 'linguatec_lexicon_frontend/search_results.html', context)


class WordDetailView(LinguatecBaseView):
    """Display a word."""
    template_name = "linguatec_lexicon_frontend/search_results.html"

    def dispatch(self, request, *args, **kwargs):
        """Retrieve and display a word by ID."""
        pk = kwargs.get('pk')
        context = self.get_context_data(**kwargs)

        api_url = settings.LINGUATEC_LEXICON_API_URL
        client = coreapi.Client()
        schema = client.get(api_url)
        url = schema['words'] + '{pk}/'.format(pk=pk)

        word = client.get(url)
        self.groupby_word_entries(word)

        url = schema['lexicons']
        response = client.get(url)
        lexicons = response["results"]

        selected_lexicon = ''
        for lex in lexicons:
            if word['lexicon'] == lex['id']:
                selected_lexicon = lex['code']

        src_languages = get_source_languages(lexicons)

        lexicons = order_lexicons(src_languages, lexicons)

        self.groupby_word_entries(word)
        self.get_urls(word)

        context.update({
            'results': [word],
            'selected_lexicon': selected_lexicon,
            'lexicons': lexicons,
        })

        return TemplateResponse(request, self.template_name, context)
