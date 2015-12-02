from octopus.modules.doaj import client as doajclient
from service import models

class HarvesterWorkflow(object):

    @classmethod
    def process_account(cls, account_id):
        doaj = doajclient.DOAJv1API()
        gen = doaj.field_search_iterator("journals", "username", account_id)
        issns = []
        for journal in gen:
            issns += journal.all_issns()
        issns = list(set(issns))

        # now update the issn states
        HarvesterWorkflow.process_issn_states(account_id, issns)

        for issn in issns:
            HarvesterWorkflow.process_issn(issn)

    @classmethod
    def process_issn_states(cls, account_id, issns):
        # first check that there are state records for all the provided issns,
        # and that if they were deactivated they are now reactivated
        for issn in issns:
            state = models.HarvestState.find_by_issn(account_id, issn)
            if state is not None:
                if state.suspended:
                    state.reactivate()
                    state.save(blocking=True)
            else:
                state = models.HarvestState()
                state.issn = issn
                state.account = account_id
                state.save(blocking=True)

        # now check if there are are any other issns for this account that we haven't
        # been provided - in that case they need to be deactivated
        hss = [hs for hs in models.HarvestState.find_by_account(account_id)]    # read straight away, as the iterator can timeout
        for hs in hss:
            if hs.issn not in issns and not hs.suspended:
                state.suspend()
                state.save(blocking=True)

    @classmethod
    def process_issn(cls, issn):
        state = models.HarvestState.find_by_issn(issn)

    @classmethod
    def process_article(cls, article):
        pass