from service import workflow
from octopus.core import app, initialise
import flask.logging

if __name__ == "__main__":
    initialise()

    if app.debug:
        # Augment the default flask debug log to include a timestamp
        app.debug_log_format = (
            '-' * 80 + '\n' +
            '%(asctime)s\n'
            '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' +
            '%(message)s\n' +
            '-' * 80
        )
        flask.logging.create_logger(app)

    accs = app.config.get("API_KEYS", {}).keys()
    for account_id in accs:
        workflow.HarvesterWorkflow.process_account(account_id)
