from gcf_data_mapper.parsers.document import document


def test_document_mapping_successful_with_valid_data(mock_gcf_docs, mock_projects_data):
    result = document(mock_projects_data, mock_gcf_docs, [], debug=False)
    assert isinstance(result, list)


def test_document_no_merge(mock_gcf_docs, mock_projects_data):
    mock_gcf_docs = mock_gcf_docs.assign(**{"FP number": ["FP125", "FP126"]})
    result = document(mock_projects_data, mock_gcf_docs, [], debug=False)
    assert all(doc is None for doc in result)


def test_document_parser_skips_documents_if_approved_ref_in_skipped_rows(
    mock_gcf_docs, mock_projects_data
):
    mock_skipped_rows = ["FP123"]
    result = document(mock_projects_data, mock_gcf_docs, mock_skipped_rows, debug=False)

    assert result == [
        {
            "family_import_id": "GCF.family.FP124.proj124",
            "import_id": "GCF.document.FP124_proj124.doc124",
            "metadata": {
                "type": [
                    "type124",
                ],
            },
            "source_url": "link124.pdf",
            "title": "title124",
            "variant_name": "Original Language",
        },
        {
            "family_import_id": "GCF.family.FP124.proj124",
            "import_id": "GCF.document.FP124_proj124.doc124",
            "metadata": {
                "type": [
                    "type124",
                ],
            },
            "source_url": "file124_fr",
            "title": "title124",
            "variant_name": "Translation",
        },
    ]
