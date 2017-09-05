from service import workflow
from octopus.core import app, initialise
from models import HarvesterProgressReport as Report
import flask.logging

from setproctitle import setproctitle
import psutil, time, datetime

STARTING_PROCTITLE = app.config.get('STARTING_PROCTITLE', 'harvester: starting')
RUNNING_PROCTITLE = app.config.get('RUNNING_PROCTITLE', 'harvester: running')
MAX_WAIT = app.config.get('MAX_WAIT', 10)


def run_only_once():
    # Identify running harvester instances.
    setproctitle(STARTING_PROCTITLE)
    running_harvesters = []
    starting_harvesters = []
    for p in psutil.process_iter():
        try:
            if p.cmdline() and p.cmdline()[0] == RUNNING_PROCTITLE:
                running_harvesters.append(p)
            if p.cmdline() and p.cmdline()[0] == STARTING_PROCTITLE:
                starting_harvesters.append(p)
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

    if len(starting_harvesters) > 1:
        print "Harvester is already starting. Aborting this instance."
        exit(1)

    # Send SIGTERM to all extant instances of the harvester.
    if len(running_harvesters) > 0:
        print "Sending SIGTERM to extant harvester instances."
        [h.terminate() for h in running_harvesters]

    # Check if they terminated correctly
    started = datetime.datetime.utcnow()
    still_running = filter(lambda hrv: hrv.is_running(), running_harvesters)
    while len(still_running) > 0 and datetime.datetime.utcnow() - started < datetime.timedelta(minutes=MAX_WAIT):
        time.sleep(10)
        still_running = filter(lambda hrv: hrv.is_running(), running_harvesters)

    # Move on to killing the processes if they don't respond to terminate
    if len(still_running) > 0:
        print "Old Harvesters are still running. Escalating to SIGKILL."
        [h.kill() for h in running_harvesters]
        time.sleep(10)

    # Startup complete, change process name to running.
    setproctitle(RUNNING_PROCTITLE)

if __name__ == "__main__":
    run_only_once()
    initialise()

    # Send an email when the harvester starts.
    mail_prereqs = False
    if app.config.get("EMAIL_ON_EVENT", False):
        to = app.config.get("EMAIL_RECIPIENTS", None)

        if to is not None:
            mail_prereqs = True
            from octopus.lib import mail
            mail.send_mail(
                to=to,
                subject="DOAJ Harvester started at {0}".format(datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")),
                msg_body="A new running instance of the harvester has started."
            )

    if app.debug:
        # Augment the default flask debug log to include a timestamp.
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

    report = Report.write_report()
    app.logger.info(report)

    # If the harvester finishes normally, we can email the report.
    if mail_prereqs:
        mail.send_mail(
            to=app.config["EMAIL_RECIPIENTS"],
            subject="DOAJ Harvester finished at {0}".format(datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")),
            msg_body=report
        )
