from functools import wraps
import signal
from octopus.core import app


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
            exit(1)

    return decorated_fn
