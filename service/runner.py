from service import workflow
from octopus.core import app, initialise

from setproctitle import setproctitle
import psutil, time, datetime


def run_only_once():
    startingproctitle = 'harvester: starting'
    runningproctitle = 'harvester: running'
    maxwait = 10                                                            # minutes we wait between terminate and kill

    # identify running harvester instances
    setproctitle(startingproctitle)
    running_harvesters = []
    starting_harvesters = []
    for p in psutil.process_iter():
        try:
            if runningproctitle in p.cmdline():
                running_harvesters.append(p)
            if startingproctitle in p.cmdline():
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
    while len(still_running) > 0 and datetime.datetime.utcnow() - started < datetime.timedelta(minutes=maxwait):
        time.sleep(10)
        still_running = filter(lambda hrv: hrv.is_running(), running_harvesters)

    # move on to killing the processes if they don't respond to terminate
    if len(still_running) > 0:
        [h.kill() for h in running_harvesters]
        time.sleep(10)

    # startup complete, change process name to running
    setproctitle(runningproctitle)

if __name__ == "__main__":
    run_only_once()
    initialise()
    accs = app.config.get("API_KEYS", {}).keys()
    for account_id in accs:
        workflow.HarvesterWorkflow.process_account(account_id)
