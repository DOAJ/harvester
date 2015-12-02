# so that your models can all be accessed from service.models, you can import them here
# like this ...
# now you can do
# from service.models import MyObject
from service.models.harvester import HarvesterPlugin, HarvestState
from service.models.epmc import EPMCHarvester