import logging
import threading
import time
from typing import Callable

from config import FAST_SCAN_INTERVAL, FULL_SCAN_INTERVAL

logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self):
        self._threads: list[threading.Thread] = []
        self._stop_event = threading.Event()

    def _loop(self, interval: int, func: Callable, name: str):
        logger.info("Scheduler thread %s started with interval %ss", name, interval)
        while not self._stop_event.is_set():
            start = time.time()
            try:
                func()
            except Exception:
                logger.exception("Error in scheduled task %s", name)
            elapsed = time.time() - start
            sleep_for = max(0, interval - elapsed)
            if self._stop_event.wait(sleep_for):
                break
        logger.info("Scheduler thread %s stopped", name)

    def start(self, fast_task: Callable, full_task: Callable):
        t_fast = threading.Thread(
            target=self._loop,
            args=(FAST_SCAN_INTERVAL, fast_task, "fast_scan"),
            daemon=True,
        )
        t_full = threading.Thread(
            target=self._loop,
            args=(FULL_SCAN_INTERVAL, full_task, "full_scan"),
            daemon=True,
        )
        self._threads.extend([t_fast, t_full])
        t_fast.start()
        t_full.start()

    def stop(self):
        self._stop_event.set()
        for t in self._threads:
            t.join(timeout=2)
