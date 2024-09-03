from gcf_data_mapper.parsers.event import event


def test_returns_empty_when_cols_missing(required_cols_missing):
    event_data = event(required_cols_missing, debug=False)
    assert event_data == []


def test_success_with_valid_data(valid_data):
    event_data = event(valid_data, debug=False)
    assert event_data == []
