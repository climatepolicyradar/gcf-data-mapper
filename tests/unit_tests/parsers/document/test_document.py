import pytest

from gcf_data_mapper.parsers.document import document


@pytest.fixture
def parsed_document_data_with_translated_titles():
    return [
        {
            "metadata": {
                "type": "Policies, strategies, and guidelines",
            },
            "source_url": "https://www.greenclimate.fund/document/guidelines-enhanced-country-ownership-and-country-drivenness",
            "title": "Guidelines for enhanced country ownership and country drivenness",
            "variant_name": "Original Translation",
        },
        {
            "metadata": {
                "type": "Policies, strategies, and guidelines",
            },
            "source_url": "https://www.greenclimate.fund/sites/default/files/document/ar-guidelines-enhanced-country-ownership-country-drivenness.pdf",
            "title": "Guidelines for enhanced country ownership and country drivenness",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Policies, strategies, and guidelines",
            },
            "source_url": "https://www.greenclimate.fund/sites/default/files/document/es-guidelines-enhanced-country-ownership-country-drivenness.pdf",
            "title": "Guidelines for enhanced country ownership and country drivenness",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Policies, strategies, and guidelines",
            },
            "source_url": "https://www.greenclimate.fund/sites/default/files/document/fr-guidelines-enhanced-country-ownership-country-drivenness.pdf",
            "title": "Guidelines for enhanced country ownership and country drivenness",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Policies, strategies, and guidelines",
            },
            "source_url": "https://www.greenclimate.fund/sites/default/files/document/ru-guidelines-enhanced-country-ownership-country-drivenns.pdf",
            "title": "Guidelines for enhanced country ownership and country drivenness",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Policies, strategies, and guidelines",
            },
            "source_url": "https://www.greenclimate.fund/sites/default/files/document/zh-guidelines-enhanced-country-ownership-country-drivenns.pdf",
            "title": "Guidelines for enhanced country ownership and country drivenness",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Policies, strategies, and guidelines",
            },
            "source_url": "https://www.greenclimate.fund/document/general-principles-and-indicative-list-eligible-costs-covered-under-gcf-fees-and-project",
            "title": "General principles and indicative list of eligible costs covered "
            "under GCF fees and project management costs",
            "variant_name": "Original Translation",
        },
        {
            "metadata": {
                "type": "Policies, strategies, and guidelines",
            },
            "source_url": "https://www.greenclimate.fund/sites/default/files/document/ar-principles-list-costs-pm_0.pdf",
            "title": "General principles and indicative list of eligible costs covered "
            "under GCF fees and project management costs",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Policies, strategies, and guidelines",
            },
            "source_url": "https://www.greenclimate.fund/sites/default/files/document/es-principles-list-costs-pm.pdf",
            "title": "General principles and indicative list of eligible costs covered "
            "under GCF fees and project management costs",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Policies, strategies, and guidelines",
            },
            "source_url": "https://www.greenclimate.fund/sites/default/files/document/fr-principles-list-costs-pm.pdf",
            "title": "General principles and indicative list of eligible costs covered "
            "under GCF fees and project management costs",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Policies, strategies, and guidelines",
            },
            "source_url": "https://www.greenclimate.fund/sites/default/files/document/ru-principles-list-costs-pm.pdf",
            "title": "General principles and indicative list of eligible costs covered "
            "under GCF fees and project management costs",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Policies, strategies, and guidelines",
            },
            "source_url": "https://www.greenclimate.fund/sites/default/files/document/zh-principles-list-costs-pm.pdf",
            "title": "General principles and indicative list of eligible costs covered "
            "under GCF fees and project management costs",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Policies, strategies, and guidelines",
            },
            "source_url": "https://www.greenclimate.fund/document/climate-finance-investment-strategies",
            "title": "Framework for climate finance and investment strategies",
            "variant_name": "Original Translation",
        },
    ]


@pytest.fixture
def parsed_document_data_with_no_translated_titles():
    return [
        {
            "metadata": {
                "type": "Approved funding proposal",
            },
            "source_url": "https://www.greenclimate.fund/document/enhancing-climate-resilience-water-sector-bahrain",
            "title": "Enhancing climate resilience of the water sector in Bahrain",
            "variant_name": "Original Translation",
        },
        {
            "metadata": {
                "type": "Approved funding proposal",
            },
            "source_url": "https://www.greenclimate.fund/document/nigeria-solar-ipp-support-programme",
            "title": "Nigeria solar IPP support programme",
            "variant_name": "Original Translation",
        },
        {
            "metadata": {
                "type": "Approved funding proposal",
            },
            "source_url": "https://www.greenclimate.fund/document/sustainable-urban-development-kenya",
            "title": "Sustainable urban development in Kenya",
            "variant_name": "Original Translation",
        },
        {
            "metadata": {
                "type": "Approved funding proposal",
            },
            "source_url": "https://www.greenclimate.fund/document/renewable-energy-initiatives-india",
            "title": "Renewable energy initiatives in India",
            "variant_name": "Original Translation",
        },
    ]


def test_returns_expected_value(
    test_document_df_without_translated_docs,
    parsed_document_data_with_no_translated_titles,
):
    document_data = document(test_document_df_without_translated_docs, debug=True)
    assert document_data is not None
    assert document_data == parsed_document_data_with_no_translated_titles


def test_returns_expected_value_for_translated_titles(
    test_document_df_with_translated_docs, parsed_document_data_with_translated_titles
):
    document_data = document(test_document_df_with_translated_docs, debug=True)
    assert document_data is not None
    assert document_data == parsed_document_data_with_translated_titles


def test_raises_error_on_missing_columns(test_df):
    with pytest.raises(ValueError) as e:
        document(test_df, debug=True)
    assert str(e.value) == ("Missing required columns in MCF data frame")


def test_raises_error_on_invalid_urls(test_document_df_with_invalid_urls):
    doc_id = test_document_df_with_invalid_urls.iloc[
        0, 0
    ]  # This is the id of the row, there is only one item
    with pytest.raises(ValueError) as e:
        document(test_document_df_with_invalid_urls, debug=True)
    assert str(e.value) == (
        f"Malformed url found in list of translated urls. DocumentId : {doc_id}"
    )


def test_raises_error_on_duplicate_urls(test_document_df_with_duplicate_urls):
    doc_id = test_document_df_with_duplicate_urls.iloc[0, 0]
    with pytest.raises(ValueError) as e:
        document(test_document_df_with_duplicate_urls, debug=True)
    assert str(e.value) == (
        f"Duplicate URLs found in list of translated urls. DocumentId : {doc_id}"
    )


def test_raises_error_on_empty_url(test_document_df_with_empty_url):
    doc_id = test_document_df_with_empty_url.iloc[0, 0]
    with pytest.raises(ValueError) as e:
        document(test_document_df_with_empty_url, debug=True)
    assert str(e.value) == (
        f"Empty URL found in list of translated urls. DocumentId : {doc_id}"
    )
