"""
Templatetags helpers to render lexicon content.
"""
import coreapi
import urllib.parse

from django import template
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from linguatec_lexicon_frontend import utils, validators


register = template.Library()


@register.filter
@stringfilter
def render_entry(value):
    """Parse entry content to apply weight to content."""
    # mark content in parenthesis
    try:
        validators.validate_balanced_parenthesis(value)
    except ValidationError:
        return value

    value = value.replace("(", "<span class='rg-usecase-comment'>(")
    value = value.replace(")", ")</span>")

    # mark keywords (inline gramcat)
    for gramcat in utils.retrieve_gramcats():
        abbr, title = gramcat['abbreviation'], gramcat['title']
        value = value.replace(
            abbr, "<span class='rg-word-gramcat' title='{0}'>{1}</span>".format(title, abbr))
    return mark_safe(value)


@register.filter
@stringfilter
def verbose_gramcat(value):
    """Attach description to gramatical category abbreviature."""
    api_url = settings.LINGUATEC_LEXICON_API_URL
    client = coreapi.Client()
    schema = client.get(api_url)
    querystring_args = {'abbr': value}
    url = urllib.parse.urljoin(
        schema['gramcats'], 'show/?' + urllib.parse.urlencode(querystring_args))
    gramcat = client.get(url)

    return "{} ({})".format(gramcat['title'], gramcat['abbreviation'])
