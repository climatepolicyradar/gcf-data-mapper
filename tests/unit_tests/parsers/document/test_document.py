import pytest

from gcf_data_mapper.parsers.document import document


@pytest.mark.parametrize("debug", [True, False])
def test_returns_empty(debug: bool):
    document_data = document(debug)
    assert document_data == []
