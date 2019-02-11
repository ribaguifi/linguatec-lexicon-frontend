import coreapi
import urllib.parse
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView


def linguatec_home(request):
    context = {}
    return TemplateResponse(request, 'linguatec_lexicon_frontend/home.html', context)


def linguatec_search(request):
    context = {}
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


class LegalNoticeView(TemplateView):
    template_name = "linguatec_lexicon_frontend/legal-notice.html"
