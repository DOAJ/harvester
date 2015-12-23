from service import workflow
from octopus.core import app, initialise

if __name__ == "__main__":
    initialise()
    accs = app.config.get("API_KEYS", {}).keys()
    for account_id in accs:
        workflow.HarvesterWorkflow.process_account(account_id)
