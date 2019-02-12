import coreapi
import urllib.parse

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
@stringfilter
def verbose_gramcat(value):
    api_url = settings.LINGUATEC_LEXICON_API_URL
    client = coreapi.Client()
    schema = client.get(api_url)
    querystring_args = {'abbr': value}
    url = urllib.parse.urljoin(schema['gramcats'], 'show/?' + urllib.parse.urlencode(querystring_args))
    gramcat = client.get(url)

    return "{} ({})".format(gramcat['title'], gramcat['abbreviation'])
