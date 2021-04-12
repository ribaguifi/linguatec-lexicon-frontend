"""
Utils to retrieve information of the lexicon backend API.
"""
import coreapi
import urllib.parse

from django.conf import settings


def removesuffix(string, suffix):
    # suffix='' should not call self[:-0].
    if suffix and string.endswith(suffix):
        return string[:-len(suffix)]
    else:
        return string[:]


def is_regular_verb(word):
    ARAGONESE_VERB_SUFFIXES = ['ar', 'er', 'ir']
    GRAMCATS_REGULAR_VERBS = [
        "v.",
        "v. cop.",
        "v. intr.",
        "v. prnl.",
        "v. reciproc.",
        "v. tr.",
    ]
    PRONOMINOADVERBIALS = ['-bi', '-ie', '-ne']

    gramcat_is_regular_verb = False
    for gramcat in word["gramcats"]:
        if gramcat in GRAMCATS_REGULAR_VERBS:
            gramcat_is_regular_verb = True
            break

    if not gramcat_is_regular_verb:
        return False

    # Detect if this term could be conjugated using softaragones conchugator
    word_root = word["term"]
    for suffix in PRONOMINOADVERBIALS:
        word_root = removesuffix(word_root, suffix)

    suffix = word_root[-2:]
    if suffix not in ARAGONESE_VERB_SUFFIXES:
        suffix = word_root[-3:]
        if suffix != '-se':
            return False

    return True


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


def retrieve_near_words(query, lex):
    """Retrieve near words of a query string through the API."""
    api_url = settings.LINGUATEC_LEXICON_API_URL
    client = coreapi.Client()
    schema = client.get(api_url)
    querystring_args = {'q': query, 'l': lex}
    url = schema['words'] + 'near/?' + urllib.parse.urlencode(querystring_args)
    response = client.get(url)
    results = response["results"]

    return results
