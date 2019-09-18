"""
from octopus.modules.doaj import models

a = models.Article()
a.bibjson = {"title" : "whatever"}
print a.bibjson.title
"""

"""
Harvest the article records from EPMC
from service.models import EPMCHarvester
h = EPMCHarvester()
r = [x for x in h.iterate("2047-2978", "2015-01-01T00:00:00Z")]
"""

from octopus.core import app, initialise
initialise()

from service.workflow import HarvesterWorkflow
from service.models import HarvesterProgressReport
try:
    HarvesterWorkflow.process_issn("15449173", "1932-6203")
finally:
    print(HarvesterProgressReport.write_report())