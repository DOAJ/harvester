"""
Unit tests for the DOAJ client
"""

from octopus.modules.es.testindex import ESTestCase
from service.tests import fixtures
from service import models

class TestDOAJ(ESTestCase):
    def setUp(self):
        super(TestDOAJ, self).setUp()

    def tearDown(self):
        super(TestDOAJ, self).tearDown()

    def test_01_harvest_state_do(self):
        # make one blank and play with its methods
        hs = models.HarvestState()
        hs.account = "abcdefg"
        hs.issn = "9876-5432"
        hs.status = "suspended"
        assert hs.account == "abcdefg"
        assert hs.issn == "9876-5432"
        assert hs.status == "suspended"
        assert hs.suspended

        hs.reactivate()
        assert not hs.suspended
        hs.suspend()
        assert hs.suspended

        hs.save(blocking=True)

        hs2 = models.HarvestState.pull(hs.id)
        assert hs.account == "abcdefg"
        assert hs.issn == "9876-5432"
        assert hs.status == "suspended"
        assert hs.suspended

        # make one from source
        source = fixtures.HarvestStateFactory.harvest_state()
        hs3 = models.HarvestState(source)
        hs3.save()