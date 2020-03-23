from transaction_service.utils import transpose_event
import pytest


def test_should_return_dictionary_when_byte_stream_provided():
    event = b'{"accountNumber": "2344234", "name": "john"}'
    assert type(transpose_event(event)) is dict
    assert transpose_event(event)['name'] == 'john'
    assert transpose_event(event)['accountNumber'] == '2344234'


def test_should_raise_error_when_baddly():
    with pytest.raises(Exception):
        event = b'{"accountNumber"}'
        transpose_event(event)
