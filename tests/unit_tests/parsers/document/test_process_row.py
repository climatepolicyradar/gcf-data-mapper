import pandas as pd
import pytest

from gcf_data_mapper.enums.document import (
    RequiredDocumentColumns,
    RequiredFamilyDocumentColumns,
    TranslatedDocumentColumns,
)
from gcf_data_mapper.parsers.document import process_row


@pytest.fixture
def mock_row():
    return pd.Series(
        {
            RequiredFamilyDocumentColumns.APPROVED_REF.value: "ref123",
            RequiredFamilyDocumentColumns.PROJECTS_ID.value: "proj123",
            RequiredDocumentColumns.ID.value: "doc123",
            RequiredDocumentColumns.TYPE.value: "type123",
            RequiredDocumentColumns.TITLE.value: "title123",
            TranslatedDocumentColumns.SOURCE_URL.value: "link123,link456",
            TranslatedDocumentColumns.TRANSLATED_FILES.value: "url123|url456",
            TranslatedDocumentColumns.TRANSLATED_TITLES.value: "title123|title456",
        }
    )


def test_process_row_success(mock_row):
    result = process_row(mock_row, debug=False)
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
