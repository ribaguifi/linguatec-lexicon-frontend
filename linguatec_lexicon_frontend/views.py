from django.shortcuts import render
from django.template.response import TemplateResponse


def linguatec_home(request):
    context = {}
    return TemplateResponse(request, 'linguatec_lexicon_frontend/home.html', context)

def linguatec_search(request):
    context = {}
    return TemplateResponse(request, 'linguatec_lexicon_frontend/search_results.html', context)