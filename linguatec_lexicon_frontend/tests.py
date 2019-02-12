from django.test import TestCase

from linguatec_lexicon_frontend.templatetags import linguatec


class RenderEntryTestCase(TestCase):
    def test_render(self):
        value = "boira (lorem ipsum)"
        html = linguatec.render_entry(value)
        self.assertInHTML("<span class='rg-usecase-comment'>(lorem ipsum)</span>", html)

    def test_render_begin(self):
        value = "(foo) boira grasa"
        html = linguatec.render_entry(value)
        self.assertInHTML("<span class='rg-usecase-comment'>(foo)</span>", html)

    def test_render_unbalanced_parenthesis(self):
        value = "(foo)) invalid"
        html = linguatec.render_entry(value)
        self.assertEqual(value, html)
