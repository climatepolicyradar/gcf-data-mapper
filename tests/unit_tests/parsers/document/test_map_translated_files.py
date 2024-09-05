import pandas as pd
import pytest

from gcf_data_mapper.enums.document import (
    RequiredDocumentColumns,
    TranslatedDocumentColumns,
)
from gcf_data_mapper.parsers.document import map_translated_files


@pytest.mark.parametrize(
    ("valid_doc_row", "expected_objects"),
    [
        ("mock_valid_doc_row_with_one_translation", 1),
        ("mock_valid_doc_row_with_two_translations", 2),
        ("mock_valid_doc_row_with_many_translations", 3),
    ],
)
def test_translated_files_mapped_to_documents(valid_doc_row, expected_objects, request):
    result = map_translated_files(request.getfixturevalue(valid_doc_row))
    assert result is not None
    assert len(result) == expected_objects


def test_translated_files_not_mapped_with_invalid_urls():
    row = pd.Series(
        {
            TranslatedDocumentColumns.TRANSLATED_FILES.value: "http://example.com|",
            RequiredDocumentColumns.ID.value: "doc123",
        }
    )
    assert map_translated_files(row) is None
