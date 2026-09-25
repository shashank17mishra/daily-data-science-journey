import json
import logging
import sys
import pytest
from learning.python.day_029_logging_architecture import (
    StructuredJSONFormatter,
    ContextFilter,
    MemoryRingBufferHandler,
    set_log_context,
    clear_log_context
)

def test_structured_json_formatter_standard_fields():
    formatter = StructuredJSONFormatter()
    record = logging.LogRecord(
        name='test_logger',
        level=logging.INFO,
        pathname='test_file.py',
        lineno=10,
        msg='User %s logged in',
        args=('alice',),
        exc_info=None
    )
    
    formatted = formatter.format(record)
    data = json.loads(formatted)
    
    assert data['level'] == 'INFO'
    assert data['logger'] == 'test_logger'
    assert data['message'] == 'User alice logged in'
    assert 'timestamp' in data
    assert 'extra' not in data

def test_structured_json_formatter_extra_fields():
    formatter = StructuredJSONFormatter()
    record = logging.LogRecord(
        name='test_logger',
        level=logging.WARNING,
        pathname='test_file.py',
        lineno=20,
        msg='Resource limit reached',
        args=(),
        exc_info=None
    )
    # Inject custom extra attributes
    record.custom_id = 'abc-123'
    record.threshold = 0.95
    
    formatted = formatter.format(record)
    data = json.loads(formatted)
    
    assert data['extra']['custom_id'] == 'abc-123'
    assert data['extra']['threshold'] == 0.95

def test_structured_json_formatter_exception():
    formatter = StructuredJSONFormatter()
    try:
        raise ValueError('Invalid configuration parameter')
    except ValueError:
        exc_info = sys.exc_info()
        
    record = logging.LogRecord(
        name='test_logger',
        level=logging.ERROR,
        pathname='test_file.py',
        lineno=30,
        msg='An error occurred',
        args=(),
        exc_info=exc_info
    )
    
    formatted = formatter.format(record)
    data = json.loads(formatted)
    
    assert 'exception' in data
    assert data['exception']['type'] == 'ValueError'
    assert 'Invalid configuration parameter' in data['exception']['message']
    assert 'traceback' in data['exception']['stacktrace'].lower()

def test_context_filter_injection():
    clear_log_context()
    set_log_context(request_id='req-999', user_id=42)
    
    ctx_filter = ContextFilter()
    record = logging.LogRecord(
        name='test_logger',
        level=logging.INFO,
        pathname='test_file.py',
        lineno=40,
        msg='Processing request',
        args=(),
        exc_info=None
    )
    
    assert not hasattr(record, 'request_id')
    ctx_filter.filter(record)
    assert record.request_id == 'req-999'
    assert record.user_id == 42
    
    clear_log_context()

def test_memory_ring_buffer_handler_capacity():
    handler = MemoryRingBufferHandler(capacity=3)
    formatter = StructuredJSONFormatter()
    handler.setFormatter(formatter)
    
    logger = logging.getLogger('ring_buffer_test')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    # Log 5 messages; only the last 3 should be retained
    for i in range(5):
        logger.info(f'Log message {i}')
        
    records = handler.get_records()
    assert len(records) == 3
    
    # Verify FIFO behavior of the ring buffer
    msg_0 = json.loads(records[0])
    msg_1 = json.loads(records[1])
    msg_2 = json.loads(records[2])
    
    assert msg_0['message'] == 'Log message 2'
    assert msg_1['message'] == 'Log message 3'
    assert msg_2['message'] == 'Log message 4'
    
    logger.removeHandler(handler)
