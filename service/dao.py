from octopus.modules.es import dao
from octopus.core import app

class MyDAO(dao.ESDAO):
    __type__ = 'myobj'
