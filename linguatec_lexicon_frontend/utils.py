import coreapi
import urllib.parse

from django.conf import settings


def retrieve_gramcats():
    api_url = settings.LINGUATEC_LEXICON_API_URL
    client = coreapi.Client()
    schema = client.get(api_url)
    gramcats = client.get(schema['gramcats'])
    return gramcats
