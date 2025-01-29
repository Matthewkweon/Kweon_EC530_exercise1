import logging
import json
import sys
from datetime import datetime

class JSONEventFormatter(logging.Formatter):
    """
    A custom logging formatter that outputs logs as JSON.
    We can store an event name and event data in a structured format.
    """

    def format(self, record: logging.LogRecord) -> str:
        # Build a base dictionary for the log record
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # If our code passes `event_name` or `event_data` via the `extra` dict, store them.
        if hasattr(record, "event_name"):
            log_record["event_name"] = record.event_name
        if hasattr(record, "event_data"):
            log_record["event_data"] = record.event_data

        return json.dumps(log_record)

    def formatTime(self, record, datefmt=None):
        # Override to produce an ISO8601 timestamp (2025-01-28T14:00:00.123456)
        return datetime.fromtimestamp(record.created).isoformat()

def get_json_logger(name: str, level=logging.INFO) -> logging.Logger:
    """
    Returns a logger that uses the JSONEventFormatter, writing logs to stdout.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding multiple handlers if the logger already has one
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(JSONEventFormatter())
        logger.addHandler(console_handler)

    return logger

def track_event(logger: logging.Logger, event_name: str, event_data=None, level=logging.INFO):
    if event_data is None:
        event_data = {}

    # We attach our custom fields via the 'extra' parameter
    logger.log(level, f"Event: {event_name}", extra={
        "event_name": event_name,
        "event_data": event_data
    })
