"""
Unit tests.
"""

import unittest

from unittest import mock

from linguatec_lexicon_frontend.templatetags import linguatec
from linguatec_lexicon_frontend.utils import is_regular_verb


class RenderEntryTestCase(unittest.TestCase):
    @mock.patch('linguatec_lexicon_frontend.utils.retrieve_gramcats')
    def test_render(self, retrieve_gramcats):
        retrieve_gramcats.return_value = []
        value = "boira (lorem ipsum)"
        html = linguatec.render_entry(value)
        self.assertIn("<span class='rg-usecase-comment'>(lorem ipsum)</span>", html)

    @mock.patch('linguatec_lexicon_frontend.utils.retrieve_gramcats')
    def test_render_begin(self, retrieve_gramcats):
        retrieve_gramcats.return_value = []
        value = "(foo) boira grasa"
        html = linguatec.render_entry(value)
        self.assertIn("<span class='rg-usecase-comment'>(foo)</span>", html)

    def test_render_unbalanced_parenthesis(self):
        value = "(foo)) invalid"
        html = linguatec.render_entry(value)
        self.assertEqual(value, html)


class IsRegularVerbTestCase(unittest.TestCase):
    def test_suffix_ar(self):
        word = {
            "gramcats": ["v."],
            "term": "chugar",
        }
        self.assertTrue(is_regular_verb(word))

    def test_suffix_pronominoadv(self):
        word = {
            "gramcats": ["v. prnl."],
            "term": "fer-se-ne",
        }
        self.assertTrue(is_regular_verb(word))

    def test_not_verb(self):
        word = {
            "gramcats": ["s."],
            "term": "mercader",
        }
        self.assertFalse(is_regular_verb(word))
