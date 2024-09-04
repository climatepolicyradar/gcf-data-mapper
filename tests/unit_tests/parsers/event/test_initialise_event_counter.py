from gcf_data_mapper.parsers.event import initialise_event_counter


def test_initialise_event_counter_adds_new_key():
    event_counter = {}
    initialise_event_counter(event_counter, "GCF.event.FP123.PID456")
    assert event_counter["GCF.event.FP123.PID456"] == 0


def test_initialise_event_counter_does_not_overwrite_existing_key():
    event_counter = {"GCF.event.FP123.PID456": 5}
    initialise_event_counter(event_counter, "GCF.event.FP123.PID456")
    assert event_counter["GCF.event.FP123.PID456"] == 5


def test_initialise_event_counter_handles_empty_key():
    event_counter = {}
    initialise_event_counter(event_counter, "")
    assert event_counter[""] == 0
