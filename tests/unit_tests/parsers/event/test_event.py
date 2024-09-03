import pytest

from gcf_data_mapper.parsers.event import event


def test_returns_empty_when_cols_missing(required_cols_missing):
    with pytest.raises(AttributeError):
        event(required_cols_missing, debug=False)


def test_success_with_valid_data(valid_data):
    event_data = event(valid_data, debug=False)
    assert event_data == []
