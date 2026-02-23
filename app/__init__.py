import logging

from flask import Flask

from config import LOG_FILE, LOG_FORMAT, LOG_LEVEL, APP_NAME
from .routes import bp, scheduled_fast_scan, scheduled_full_scan
from .scheduler import Scheduler


scheduler: Scheduler | None = None


def create_app() -> Flask:
    global scheduler

    # Logging
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting %s application", APP_NAME)

    app = Flask(__name__)
    app.register_blueprint(bp)

    # Start background scheduler
    scheduler = Scheduler()
    scheduler.start(
        fast_task=scheduled_fast_scan,
        full_task=scheduled_full_scan,
    )

    @app.before_first_request
    def _log_ready():
        logger.info("%s is ready to accept requests", APP_NAME)

    return app
