from gcf_data_mapper.parsers.document import document


def test_document_mapping_successful_with_valid_data(mock_gcf_docs, mock_projects_data):
    result = document(mock_projects_data, mock_gcf_docs, debug=False)
    assert isinstance(result, list)


def test_document_no_merge(mock_gcf_docs, mock_projects_data):
    mock_gcf_docs = mock_gcf_docs.assign(**{"FP number": ["FP125", "FP126"]})
    result = document(mock_projects_data, mock_gcf_docs, debug=False)
    assert all(doc is None for doc in result)
