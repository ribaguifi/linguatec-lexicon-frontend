"""
Utils to retrieve information of the lexicon backend API.
"""
import coreapi
import urllib.parse

from django.conf import settings


def retrieve_gramcats():
    """Retrieve all the gramatical categories through the API."""
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


def retrieve_near_words(query):
    """Retrieve near words of a query string through the API."""
    api_url = settings.LINGUATEC_LEXICON_API_URL
    client = coreapi.Client()
    schema = client.get(api_url)
    querystring_args = {'q': query}
    url = schema['words'] + 'near/?' + urllib.parse.urlencode(querystring_args)
    response = client.get(url)
    results = response["results"]

    return results
