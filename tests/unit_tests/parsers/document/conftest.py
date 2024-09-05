import pandas as pd
import pytest

from gcf_data_mapper.enums.document import (
    RequiredDocumentColumns,
    RequiredFamilyDocumentColumns,
    TranslatedDocumentColumns,
)


@pytest.fixture
def mock_valid_doc_row_with_one_translation():
    return pd.Series(
        {
            RequiredFamilyDocumentColumns.APPROVED_REF.value: "ref123",
            RequiredFamilyDocumentColumns.PROJECTS_ID.value: "proj123",
            RequiredDocumentColumns.ID.value: "doc123",
            RequiredDocumentColumns.TYPE.value: "type123",
            RequiredDocumentColumns.TITLE.value: "title123",
            TranslatedDocumentColumns.SOURCE_URL.value: "link123",
            TranslatedDocumentColumns.TRANSLATED_FILES.value: "http://example.com",
            TranslatedDocumentColumns.TRANSLATED_TITLES.value: "title123",
        }
    )


@pytest.fixture
def mock_valid_doc_row_with_many_translations():
    return pd.Series(
        {
            RequiredFamilyDocumentColumns.APPROVED_REF.value: "ref123",
            RequiredFamilyDocumentColumns.PROJECTS_ID.value: "proj123",
            RequiredDocumentColumns.ID.value: "doc123",
            RequiredDocumentColumns.TYPE.value: "type123",
            RequiredDocumentColumns.TITLE.value: "title123",
            TranslatedDocumentColumns.SOURCE_URL.value: "link123,link456,link789",
            TranslatedDocumentColumns.TRANSLATED_FILES.value: "http://example.com|http://example.org|http://example.co.uk",
            TranslatedDocumentColumns.TRANSLATED_TITLES.value: "title123|title456|title789",
        }
    )


@pytest.fixture
def mock_valid_doc_row_with_two_translations():
    return pd.Series(
        {
            RequiredFamilyDocumentColumns.APPROVED_REF.value: "ref123",
            RequiredFamilyDocumentColumns.PROJECTS_ID.value: "proj123",
            RequiredDocumentColumns.ID.value: "doc123",
            RequiredDocumentColumns.TYPE.value: "type123",
            RequiredDocumentColumns.TITLE.value: "title123",
            TranslatedDocumentColumns.SOURCE_URL.value: "link123,link456",
            TranslatedDocumentColumns.TRANSLATED_FILES.value: "http://example.com|http://example.org",
            TranslatedDocumentColumns.TRANSLATED_TITLES.value: "title123|title456",
        }
    )
