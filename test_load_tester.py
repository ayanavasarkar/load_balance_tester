import pytest
from load_tester import LoadTester
from unittest.mock import patch, MagicMock

# Test initialization
def test_load_tester_initialization():
    kwargs = {
        'url': 'http://google.com',
        'qps': 10,
        'timeout': 5.0,
        'max_requests': 100,
        'method': 'GET',
        'headers': {'Content-Type': 'application/json'},
        'payload': {'key': 'value'},
        'logging': True,
        'percentiles': [90, 95, 99],
        'response_thres': [],
    }
    load_tester = LoadTester(kwargs)
    assert load_tester.url == kwargs['url']
    assert load_tester.qps == kwargs['qps']
    assert load_tester.timeout == kwargs['timeout']
    assert load_tester.method == kwargs['method'].upper()
    assert load_tester.headers == kwargs['headers']
    assert load_tester.payload == kwargs['payload']
    assert load_tester.errors == 0
    assert load_tester.latencies == []
    assert load_tester.max_requests == kwargs['max_requests']
    assert load_tester.request_count == 0
    assert load_tester.log_enabled == kwargs['logging']
    assert load_tester.percentiles == kwargs['percentiles']

#Test request method
def test_request_method():
    kwargs = {
        'url': 'http://google.com',
        'qps': 10,
        'timeout': 5.0,
        'max_requests': 100,
        'method': 'GET',
        'headers': {'Content-Type': 'application/json'},
        'payload': {'key': 'value'},
        'logging': True,
        'percentiles': [90, 95, 99],
        'response_thres': [],
    }
    load_tester = LoadTester(kwargs)
    load_tester.request()
    assert load_tester.request_count == 1
    assert len(load_tester.latencies) == 1

def test_request_method_successful_request():
    # Create a mock response object
    response_mock = MagicMock()
    response_mock.status_code = 200
    kwargs = {
        'url': 'http://google.com',
        'qps': 10,
        'timeout': 5.0,
        'max_requests': 100,
        'method': 'GET',
        'headers': {'Content-Type': 'application/json'},
        'payload': {'key': 'value'},
        'logging': True,
        'percentiles': [90, 95, 99],
        'response_thres': [],
    }
    # Mock the requests.request function to return the mock response
    with patch('requests.request', return_value=response_mock):
        
        load_tester = LoadTester(kwargs)
        load_tester.request()

    # Check if latency and errors are recorded correctly
    assert len(load_tester.latencies) == 1
    assert load_tester.errors == 0

def test_request_method_logging_enabled():
    kwargs = {
        'url': 'http://google.com',
        'qps': 10,
        'timeout': 5.0,
        'max_requests': 100,
        'method': 'GET',
        'headers': {'Content-Type': 'application/json'},
        'payload': {'key': 'value'},
        'logging': True,
        'percentiles': [90, 95, 99],
        'response_thres': [],
    }
    # Create a mock response object
    response_mock = MagicMock()
    response_mock.status_code = 200

    # Mock the requests.request function to return the mock response
    with patch('requests.request', return_value=response_mock):
        load_tester = LoadTester(kwargs)
        load_tester.log_request = MagicMock()

        load_tester.request()

    # Check if log_request method is called
    assert load_tester.log_request.called

def test_request_method_logging_disabled():
    kwargs = {
        'url': 'http://google.com',
        'qps': 10,
        'timeout': 5.0,
        'max_requests': 100,
        'method': 'GET',
        'headers': {'Content-Type': 'application/json'},
        'payload': {'key': 'value'},
        'logging': False,
        'percentiles': [90, 95, 99],
        'response_thres': [],
    }
    # Create a mock response object
    response_mock = MagicMock()
    response_mock.status_code = 200

    # Mock the requests.request function to return the mock response
    with patch('requests.request', return_value=response_mock):
        load_tester = LoadTester(kwargs)
        load_tester.log_request = MagicMock()

        load_tester.request()

    # Check if log_request method is not called
    assert not load_tester.log_request.called
