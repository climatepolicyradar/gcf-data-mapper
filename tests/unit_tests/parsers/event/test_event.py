import pytest

from gcf_data_mapper.parsers.event import event


@pytest.mark.parametrize("debug", [True, False])
def test_returns_empty(test_df, debug: bool):
    event_data = event(test_df, debug)
    assert event_data == []
