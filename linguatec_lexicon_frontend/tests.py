import unittest

from unittest import mock

from linguatec_lexicon_frontend.templatetags import linguatec


class RenderEntryTestCase(unittest.TestCase):
    @unittest.mock.patch('linguatec_lexicon_frontend.utils.retrieve_gramcats')
    def test_render(self, retrieve_gramcats):
        retrieve_gramcats.return_value = []
        value = "boira (lorem ipsum)"
        html = linguatec.render_entry(value)
        self.assertIn("<span class='rg-usecase-comment'>(lorem ipsum)</span>", html)

    @unittest.mock.patch('linguatec_lexicon_frontend.utils.retrieve_gramcats')
    def test_render_begin(self, retrieve_gramcats):
        retrieve_gramcats.return_value = []
        value = "(foo) boira grasa"
        html = linguatec.render_entry(value)
        self.assertIn("<span class='rg-usecase-comment'>(foo)</span>", html)

    def test_render_unbalanced_parenthesis(self):
        value = "(foo)) invalid"
        html = linguatec.render_entry(value)
        self.assertEqual(value, html)
