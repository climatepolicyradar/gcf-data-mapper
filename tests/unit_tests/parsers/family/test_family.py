import pytest

from gcf_data_mapper.parsers.family import family


@pytest.mark.parametrize("debug", [True, False])
def test_returns_empty(test_df, debug: bool):
    family_data = family(test_df, debug)
    assert family_data == []
