import pandas as pd
import pytest

from gcf_data_mapper.enums.document import (
    RequiredDocumentColumns,
    RequiredFamilyDocumentColumns,
    TranslatedDocumentColumns,
)
from gcf_data_mapper.parsers.document import map_translated_files


@pytest.fixture
def mock_row():
    return pd.Series(
        {
            RequiredFamilyDocumentColumns.APPROVED_REF.value: "ref123",
            RequiredFamilyDocumentColumns.PROJECTS_ID.value: "proj123",
            RequiredDocumentColumns.ID.value: "doc123",
            RequiredDocumentColumns.TYPE.value: "type123",
            RequiredDocumentColumns.TITLE.value: "title123",
            TranslatedDocumentColumns.SOURCE_URL.value: "link123",
            TranslatedDocumentColumns.TRANSLATED_FILES.value: "http://example.com|http://example.org",
        }
    )


def test_translated_files_mapped_to_documents(mock_row):
    result = map_translated_files(mock_row)
    assert len(result) == 2


def test_translated_files_not_mapped_with_invalid_urls():
    row = pd.Series(
        {
            TranslatedDocumentColumns.TRANSLATED_FILES.value: "http://example.com|",
            RequiredDocumentColumns.ID.value: "doc123",
        }
    )
    assert map_translated_files(row) is None
