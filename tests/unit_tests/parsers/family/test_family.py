import pytest

from gcf_data_mapper.parsers.family import family


@pytest.mark.parametrize("debug", [True, False])
def test_returns_empty(debug: bool):
    family_data = family(debug)
    assert family_data == []
