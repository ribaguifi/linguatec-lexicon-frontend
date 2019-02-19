import coreapi
import urllib.parse

from django.conf import settings


def retrieve_gramcats():
    api_url = settings.LINGUATEC_LEXICON_API_URL
    client = coreapi.Client()
    schema = client.get(api_url)
    querystring_args = {'limit': 100}

    response = client.get(schema['gramcats'] + '?' + urllib.parse.urlencode(querystring_args))
    gramcats = response["results"]

    # iterate over all pages to retrieve all the gramcats
    next_page = response["next"]
    while next_page:
        response = client.get(next_page)
        gramcats += response["results"]
        next_page = response["next"]

    return gramcats
