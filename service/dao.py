from octopus.modules.es import dao

class HarvestStateDAO(dao.ESDAO):
    __type__ = 'state'

    @classmethod
    def find_by_issn(cls, account, issn):
        q = ISSNQuery(account, issn)
        obs = cls.object_query(q.query())
        if len(obs) > 0:
            return obs[0]
        return None

    @classmethod
    def find_by_account(cls, account):
        q = AccountQuery(account)
        return cls.scroll(q=q.query())

    @classmethod
    def example(cls):
        from service.tests import fixtures
        return cls(fixtures.HarvestStateFactory.harvest_state())


class ISSNQuery(object):
    def __init__(self, account, issn):
        self.issn = issn
        self.account = account

    def query(self):
        return {
            "query" : {
                "bool" : {
                    "must" : [
                        {"term" : {"issn.exact" : self.issn}},
                        {"term" : {"account.exact" : self.account}}
                    ]
                }
            }
        }

class AccountQuery(object):
    def __init__(self, account):
        self.account = account

    def query(self):
        return {
            "query" : {
                "bool" : {
                    "must" : [
                        {"term" : {"account.exact" : self.account}}
                    ]
                }
            }
        }