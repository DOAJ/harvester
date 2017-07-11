from service import workflow
from octopus.core import app, initialise
import flask.logging

from setproctitle import setproctitle
import psutil, time, datetime

STARTING_PROCTITLE = 'harvester: starting'                                  # Process name while harvester is starting
RUNNING_PROCTITLE = 'harvester: running'
MAX_WAIT = 10                                                               # minutes we wait between terminate and kill


def run_only_once():
    # identify running harvester instances
    setproctitle(STARTING_PROCTITLE)
    running_harvesters = []
    starting_harvesters = []
    for p in psutil.process_iter():
        try:
            if p.cmdline()[0] == RUNNING_PROCTITLE:
                running_harvesters.append(p)
            if p.cmdline()[0] == STARTING_PROCTITLE:
                starting_harvesters.append(p)
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

    if len(starting_harvesters) > 1:
        print "Harvester is already starting. Aborting this instance."
        exit(1)

    # send SIGTERM to all extant instances of the harvester
    if len(running_harvesters) > 0:
        [h.terminate() for h in running_harvesters]

    # check if they terminated correctly
    started = datetime.datetime.utcnow()
    still_running = filter(lambda hrv: hrv.is_running(), running_harvesters)
    while len(still_running) > 0 and datetime.datetime.utcnow() - started < datetime.timedelta(minutes=MAX_WAIT):
        time.sleep(10)
        still_running = filter(lambda hrv: hrv.is_running(), running_harvesters)

    # move on to killing the processes if they don't respond to terminate
    if len(still_running) > 0:
        [h.kill() for h in running_harvesters]
        time.sleep(10)

    # startup complete, change process name to running
    setproctitle(RUNNING_PROCTITLE)

if __name__ == "__main__":
    run_only_once()
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
