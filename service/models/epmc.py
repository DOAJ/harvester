from service.models import HarvesterPlugin
from octopus.modules.epmc import client, queries
from octopus.lib import dates
from octopus.modules.doaj import models as doaj

class EPMCHarvester(HarvesterPlugin):
    def get_name(self):
        return "epmc"

    def iterate(self, issn, since, to=None):
        # set the default value for to, if not already set
        if to is None:
            to = dates.now()

        # get the dates into a datestamp
        sd = dates.parse(since)
        td = dates.parse(to)

        # calculate the ranges we're going to want to query by
        # We're going to query epmc one day at a time, so that we can effectively
        # iterate through in updated date order (though within each day, there will
        # be no ordering, there is little we can do about that except reduce the
        # request granularity further, which would massively increase the number
        # of requests)
        ranges = dates.day_ranges(sd, td)

        for fr, until in ranges:
            # build the query for the oa articles in that issn for the specified day (note we don't use the range, as the granularity in EPMC means we'd double count
            # note that we use date_sort=True as a weak proxy for ordering by updated date (it actually orders by publication date, which may be partially the same as updated date)
            query = queries.oa_issn_updated(issn, fr, date_sort=True)
            for record in client.EuropePMC.complex_search_iterator(query):
                article = self._crosswalk(record)
                yield article

    def _crosswalk(self, record):
        article = doaj.Article()
        article.bibjson = {"title" : record.title}
        return article

