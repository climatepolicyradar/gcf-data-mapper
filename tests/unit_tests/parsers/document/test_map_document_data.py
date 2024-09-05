from gcf_data_mapper.enums.document import DocumentVariantNames
from gcf_data_mapper.parsers.document import map_document_metadata


def test_map_document_metadata_with_source_url(mock_valid_row):
    source_url = "http://example.com"
    result = map_document_metadata(
        mock_valid_row, DocumentVariantNames.ORIGINAL.value, source_url
    )
    assert result["source_url"] == source_url


def test_map_document_metadata_without_source_url(mock_valid_row):
    result = map_document_metadata(mock_valid_row, DocumentVariantNames.ORIGINAL.value)
    assert (
        "source_url" in result
        and result["source_url"] == mock_valid_row["Document page permalink"]
    )
