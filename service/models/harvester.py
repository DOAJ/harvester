from octopus.lib import dataobj
from service import dao
from octopus.lib import dates

class HarvesterPlugin(object):
    def get_name(self):
        raise NotImplementedError()

    def iterate(self, issn, since, to=None):
        raise NotImplementedError()

class HarvestState(dataobj.DataObj, dao.HarvestStateDAO):
    def __init__(self, raw=None):
        struct = {
            "fields" : {
                "id" : {"coerce" : "unicode"},
                "last_updated" : {"coerce" : "utcdatetime"},
                "created_date" : {"coerce" : "utcdatetime"},
                "issn" : {"coerce" : "unicode"},
                "status" : {"coerce" : "unicode", "allowed_values" : [u"suspended", u"active"]},
                "account" : {"coerce" : "unicode"},
            },
            "lists" : {
                "last_harvest" : {"contains" : "object"}
            },

            "structs" : {
                "last_harvest" : {
                    "fields" : {
                        "plugin" : {"coerce" : "unicode"},
                        "date" : {"coerce" : "utcdatetime"}
                    }
                }
            }
        }

        super(HarvestState, self).__init__(raw, struct)

    def _coerce_and_kwargs(self, path, dir):
        type, struct, instructions = dataobj.construct_lookup(path, self._struct)
        c = self._coerce_map.get(instructions.get("coerce", "unicode"))
        kwargs = dataobj.construct_kwargs(type, dir, instructions)
        return c, kwargs

    @property
    def account(self):
        c, kwargs = self._coerce_and_kwargs("account", "get")
        return self._get_single("account", coerce=c, **kwargs)

    @account.setter
    def account(self, val):
        c, kwargs = self._coerce_and_kwargs("account", "set")
        self._set_single("account", val, coerce=c, **kwargs)

    @property
    def issn(self):
        c, kwargs = self._coerce_and_kwargs("issn", "get")
        return self._get_single("issn", coerce=c, **kwargs)

    @issn.setter
    def issn(self, val):
        c, kwargs = self._coerce_and_kwargs("issn", "set")
        self._set_single("issn", val, coerce=c, **kwargs)

    def suspend(self):
        self.status = "suspended"

    @property
    def suspended(self):
        return self.status == u"suspended"

    @property
    def status(self):
        c, kwargs = self._coerce_and_kwargs("status", "get")
        return self._get_single("status", coerce=c, **kwargs)

    @status.setter
    def status(self, val):
        c, kwargs = self._coerce_and_kwargs("status", "set")
        self._set_single("status", val, coerce=c, **kwargs)

    def reactivate(self):
        self.status = "active"

    def get_last_harvest(self, harvester_name):
        lhs = self._get_list("last_harvest")
        for lh in lhs:
            if lh.get("plugin") == harvester_name:
                return lh.get("date")
        return None

    def set_harvested(self, harvester_name, last_harvest_date=None):
        # first ensure we have a last harvest date, and that it's in the right format
        if last_harvest_date is None:
            last_harvest_date = dates.now()
        last_harvest_date = dates.reformat(last_harvest_date)

        self._delete_from_list("last_harvest", matchsub={"plugin" : harvester_name})
        self._add_to_list("last_harvest", {"plugin" : harvester_name, "date" : last_harvest_date})

    def prep(self):
        if self.status is None:
            self.status = "active"



