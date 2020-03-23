from transaction_service.mock.mock_events import MockEvents
import pytest
from unittest.mock import Mock


@pytest.fixture(scope="function")
def broker():
    broker = MockEvents()
    return broker


def test_no_events_published(broker):
    assert broker.last_event is None


def test_last_event_on_publish(broker):
    event = "Hello Event!!"
    broker.produce(event)
    assert broker.last_event is event


def test_action_on_publish(broker):
    event = "Other event"
    action = Mock()
    broker.on_event(action)
    broker.produce(event)
    action.assert_called_with(event)
