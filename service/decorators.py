from functools import wraps
import signal, datetime
from octopus.core import app
from models import HarvesterProgressReport as Report


class CaughtTermException(Exception):
    pass


def term_handler(signum, frame):
    app.logger.warning("Harvester terminated with signal " + str(signum))
    raise CaughtTermException


def capture_sigterm(fn):
    # Register the SIGTERM handler to raise an exception, allowing graceful exit.
    signal.signal(signal.SIGTERM, term_handler)

    """ Decorator which allows graceful exit on SIGTERM """
    @wraps(fn)
    def decorated_fn(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except (CaughtTermException, KeyboardInterrupt):
            app.logger.warning(u"Harvester caught SIGTERM. Exiting.")
            report = Report.write_report()
            if app.config.get("EMAIL_ON_EVENT", False):
                to = app.config.get("EMAIL_RECIPIENTS", None)

                if to is not None:
                    from octopus.lib import mail
                    mail.send_mail(
                        to=app.config["EMAIL_RECIPIENTS"],
                        subject="DOAJ Harvester caught SIGTERM at {0}".format(
                            datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")),
                        msg_body=report
                    )
            app.logger.info(report)
            exit(1)

    return decorated_fn
