"""
Unit tests for the DOAJ client
"""

from unittest import TestCase
# from octopus.modules.es.testindex import ESTestCase
from service.tests import fixtures
from octopus.modules.doaj import client as doajclient, models
from octopus.lib import dataobj

class TestDOAJ(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_journal_issns(self):
        source = fixtures.JournalFixtureFactory.journal()
        j = models.Journal(source)
        issns = j.all_issns()
        assert "1234-5678" in issns
        assert "9876-5432" in issns
        assert "4444-4444" in issns
        assert "5555-5555" in issns
        assert "0101-0101" in issns
        assert len(issns) == 5

    def test_02_validate_article(self):
        invalid = {"bibjson" : {}}

        # first check the article validator works
        with self.assertRaises(dataobj.DataStructureException):
            models.ArticleValidator(invalid)

        # then check that the api validation method works
        a = models.Article(invalid)
        assert not a.is_api_valid()

