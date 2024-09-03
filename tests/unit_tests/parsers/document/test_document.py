import pytest

from gcf_data_mapper.parsers.document import document


@pytest.fixture
def parsed_document_data_with_translated_titles():
    return [
        {
            "metadata": {
                "type": "Climate Action Plans",
            },
            "source_url": "https://www.climateprojects.org/document/renewable-energy-strategies",
            "title": "Strategies for Accelerating Renewable Energy Adoption",
            "variant_name": "Original Translation",
        },
        {
            "metadata": {
                "type": "Climate Action Plans",
            },
            "source_url": "https://www.climateprojects.org/docs/ar-renewable-energy-strategies.pdf",
            "title": "Strategies for Accelerating Renewable Energy Adoption",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Climate Action Plans",
            },
            "source_url": "https://www.climateprojects.org/docs/es-renewable-energy-strategies.pdf",
            "title": "Strategies for Accelerating Renewable Energy Adoption",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Climate Action Plans",
            },
            "source_url": "https://www.climateprojects.org/docs/fr-renewable-energy-strategies.pdf",
            "title": "Strategies for Accelerating Renewable Energy Adoption",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Climate Action Plans",
            },
            "source_url": "https://www.climate_projects.org/docs/ru-renewable-energy-strategies.pdf",
            "title": "Strategies for Accelerating Renewable Energy Adoption",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Climate Action Plans",
            },
            "source_url": "https://www.climateprojects.org/docs/zh-renewable-energy-strategies.pdf",
            "title": "Strategies for Accelerating Renewable Energy Adoption",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Climate Action Plans",
            },
            "source_url": "https://www.climateprojects.org/document/sustainable-urban-development",
            "title": "Principles and Guidelines for Sustainable Urban Development",
            "variant_name": "Original Translation",
        },
        {
            "metadata": {
                "type": "Climate Action Plans",
            },
            "source_url": "https://www.climateprojects.org/docs/ar-sustainable-urban-development.pdf",
            "title": "Principles and Guidelines for Sustainable Urban Development",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Climate Action Plans",
            },
            "source_url": "https://www.climateprojects.org/docs/es-sustainable-urban-development.pdf",
            "title": "Principles and Guidelines for Sustainable Urban Development",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Climate Action Plans",
            },
            "source_url": "https://www.climateprojects.org/docs/fr-sustainable-urban-development.pdf",
            "title": "Principles and Guidelines for Sustainable Urban Development",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Climate Action Plans",
            },
            "source_url": "https://www.climate_projects.org/docs/ru-sustainable-urban-development.pdf",
            "title": "Principles and Guidelines for Sustainable Urban Development",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Climate Action Plans",
            },
            "source_url": "https://www.climateprojects.org/docs/zh-sustainable-urban-development.pdf",
            "title": "Principles and Guidelines for Sustainable Urban Development",
            "variant_name": "Translated",
        },
        {
            "metadata": {
                "type": "Climate Action Plans",
            },
            "source_url": "https://www.climateprojects.org/document/climate-resilience-framework",
            "title": "Framework for Climate Resilience and Adaptation",
            "variant_name": "Original Translation",
        },
    ]


@pytest.fixture
def parsed_document_data_with_no_translated_titles():
    return [
        {
            "metadata": {
                "type": "Climate change mitigation project",
            },
            "source_url": "https://www.climateprojects.org/solar-power-project",
            "title": "Community-based solar power project",
            "variant_name": "Original Translation",
        },
        {
            "metadata": {
                "type": "Renewable energy initiative",
            },
            "source_url": "https://www.climateprojects.org/reforestation-program",
            "title": "Afforestation and reforestation program",
            "variant_name": "Original Translation",
        },
        {
            "metadata": {
                "type": "Sustainable agriculture program",
            },
            "source_url": "https://www.climateprojects.org/organic-farming-project",
            "title": "Organic farming and soil conservation project",
            "variant_name": "Original Translation",
        },
        {
            "metadata": {
                "type": "Carbon offset project",
            },
            "source_url": "https://www.climateprojects.org/mangrove-conservation-project",
            "title": "Mangrove restoration and conservation project",
            "variant_name": "Original Translation",
        },
    ]


def test_returns_expected_value(
    test_document_df_without_translated_docs,
    parsed_document_data_with_no_translated_titles,
):
    document_data = document(test_document_df_without_translated_docs, debug=True)
    assert document_data != []
    assert document_data == parsed_document_data_with_no_translated_titles


def test_returns_expected_value_for_translated_titles(
    test_document_df_with_translated_docs, parsed_document_data_with_translated_titles
):
    document_data = document(test_document_df_with_translated_docs, debug=True)
    assert document_data != []
    assert document_data == parsed_document_data_with_translated_titles


def test_raises_error_on_missing_columns(test_document_df):
    with pytest.raises(ValueError) as e:
        document(test_document_df, debug=True)
    assert str(e.value) == ("Missing required columns in GCF data frame")


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
