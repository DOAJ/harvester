"""
from octopus.modules.doaj import models

a = models.Article()
a.bibjson = {"title" : "whatever"}
print a.bibjson.title
"""


from service.models import EPMCHarvester
h = EPMCHarvester()
r = [x for x in h.iterate("2047-2978", "2015-01-01T00:00:00Z")]
