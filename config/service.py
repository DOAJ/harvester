##################################################
# overrides for the webapp deployment

DEBUG = True
PORT = 5000
SSL = False
THREADED = True

############################################
# important overrides for the ES module

# elasticsearch back-end connection settings
ELASTIC_SEARCH_HOST = "http://localhost:9200"
ELASTIC_SEARCH_INDEX = "doajharvester"
ELASTIC_SEARCH_VERSION = "1.4.4"

# Classes from which to retrieve ES mappings to be used in this application
# (note that if ELASTIC_SEARCH_DEFAULT_MAPPINGS is sufficient, you don't need to
# add anything here
ELASTIC_SEARCH_MAPPINGS = [
    # "service.dao.MyDAO"
]

# initialise the index with example documents from each of the types
# this will initialise each type and auto-create the relevant mappings where
# example data is provided
ELASTIC_SEARCH_EXAMPLE_DOCS = [
    "service.dao.HarvestStateDAO"
]

############################################
# important overrides for account module

ACCOUNT_ENABLE = False
SECRET_KEY = "super-secret-key"

#############################################
# important overrides for storage module

#STORE_IMPL = "octopus.modules.store.store.StoreLocal"
#STORE_TMP_IMPL = "octopus.modules.store.store.TempStore"

from octopus.lib import paths
STORE_LOCAL_DIR = paths.rel2abs(__file__, "..", "service", "tests", "local_store", "live")
STORE_TMP_DIR = paths.rel2abs(__file__, "..", "service", "tests", "local_store", "tmp")

##############################################
# DOAJ client configuration

# this is the default anyway, but reminds us to point it to the right place for testing
DOAJ_API_BASE_URL = "https://doaj.org/api/v1/"

##############################################
# Application-specific configuration

HARVESTERS = [
    "service.models.EPMCHarvester"
]

INITIAL_HARVEST_DATE = "2015-12-01T00:00:00Z"

# The mapping from account ids to API keys.  MUST NOT be checked into the repo, put these
# in the local.cfg instead
API_KEYS = {

}

EPMC_HARVESTER_THROTTLE = 0.2