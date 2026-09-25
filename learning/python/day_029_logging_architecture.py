import json
import logging
import threading
from collections import deque
from datetime import datetime, timezone
from typing import Any, Dict, List

# Thread-local storage to hold dynamic context (e.g., request IDs, user IDs)
_context = threading.local()

def set_log_context(**kwargs: Any) -> None:
    """Set dynamic context variables for the current thread."""
    if not hasattr(_context, 'data'):
        _context.data = {}
    _context.data.update(kwargs)

def clear_log_context() -> None:
    """Clear all context variables for the current thread."""
    _context.data = {}

class ContextFilter(logging.Filter):
    """
    A logging filter that injects dynamic context variables from thread-local
    storage into every LogRecord processed by the logger.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        context_data = getattr(_context, 'data', {})
        for key, val in context_data.items():
            setattr(record, key, val)
        return True

class StructuredJSONFormatter(logging.Formatter):
    """
    A custom formatter that outputs log records as single-line JSON strings.
    Automatically captures standard fields, custom extra attributes, and exceptions.
    """
    # Standard LogRecord attributes to exclude from the 'extra' payload
    STANDARD_FIELDS = {
        'name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename',
        'module', 'exc_info', 'exc_text', 'stack_info', 'lineno', 'funcName',
        'created', 'msecs', 'relativeCreated', 'thread', 'threadName',
        'processName', 'process', 'message'
    }

    def format(self, record: logging.LogRecord) -> str:
        # Ensure the message is formatted with any arguments
        record.message = record.getMessage()

        # Build base payload
        payload: Dict[str, Any] = {
            'timestamp': datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.message,
            'module': record.module,
            'line': record.lineno
        }

        # Capture exception details if present
        if record.exc_info:
            payload['exception'] = {
                'type': record.exc_info[0].__name__ if record.exc_info[0] else 'Exception',
                'message': str(record.exc_info[1]),
                'stacktrace': self.formatException(record.exc_info)
            }

        # Capture any extra attributes attached to the LogRecord
        extra: Dict[str, Any] = {}
        for key, val in record.__dict__.items():
            if key not in self.STANDARD_FIELDS and not key.startswith('_'):
                extra[key] = val

        if extra:
            payload['extra'] = extra

        return json.dumps(payload)

class MemoryRingBufferHandler(logging.Handler):
    """
    A custom in-memory handler that keeps only the last N formatted log records
    using a thread-safe ring buffer (collections.deque).
    """
    def __init__(self, capacity: int = 100, level: int = logging.NOTSET):
        super().__init__(level=level)
        self.buffer: deque = deque(maxlen=capacity)
        self._lock = threading.Lock()

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            with self._lock:
                self.buffer.append(msg)
        except Exception:
            self.handleError(record)

    def get_records(self) -> List[str]:
        """Return a list of all currently buffered log records."""
        with self._lock:
            return list(self.buffer)

    def clear(self) -> None:
        """Clear the ring buffer."""
        with self._lock:
            self.buffer.clear()
