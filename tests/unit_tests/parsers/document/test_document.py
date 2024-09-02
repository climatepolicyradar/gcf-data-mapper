import pytest

from gcf_data_mapper.parsers.document import document


@pytest.mark.parametrize("debug", [True, False])
def test_returns_empty(test_df, debug: bool):
    document_data = document(test_df, debug)
    assert document_data == []
