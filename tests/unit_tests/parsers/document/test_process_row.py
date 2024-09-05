import pandas as pd
import pytest

from gcf_data_mapper.enums.document import (
    RequiredDocumentColumns,
    RequiredFamilyDocumentColumns,
)
from gcf_data_mapper.parsers.document import process_row


@pytest.mark.parametrize(
    "valid_doc_row",
    [
        "mock_valid_doc_row_with_one_translation",
        "mock_valid_doc_row_with_two_translations",
        "mock_valid_doc_row_with_many_translations",
    ],
)
def test_process_row_with_translations_success(valid_doc_row, request):
    result = process_row(request.getfixturevalue(valid_doc_row), debug=False)
    assert isinstance(result, list)


def test_process_row_with_no_translations_success(
    mock_valid_doc_row_with_no_translations,
):
    result = process_row(mock_valid_doc_row_with_no_translations, debug=False)
    assert isinstance(result, list)


def test_process_row_returns_none_with_missing_required_columns():
    row = pd.Series(
        {
            RequiredFamilyDocumentColumns.APPROVED_REF.value: None,
            RequiredFamilyDocumentColumns.PROJECTS_ID.value: None,
            RequiredDocumentColumns.ID.value: None,
        }
    )
    assert process_row(row, debug=False) is None
