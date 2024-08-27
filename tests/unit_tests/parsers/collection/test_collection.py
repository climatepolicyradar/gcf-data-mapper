import pytest

from gcf_data_mapper.parsers.collection import collection


@pytest.mark.parametrize("debug", [True, False])
def test_returns_empty(debug: bool):
    collection_data = collection(debug)
    assert collection_data == []
