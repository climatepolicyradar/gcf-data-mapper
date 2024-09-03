import pandas as pd
import pytest


@pytest.fixture()
def test_df():
    yield pd.DataFrame(
        {
            "col1": ["record1"],
        }
    )


@pytest.fixture()
def test_document_df_without_translated_docs():
    yield pd.DataFrame(
        {
            "ID": [1234, 2345, 3456, 4567],
            "Type": [
                "Climate change mitigation project",
                "Renewable energy initiative",
                "Sustainable agriculture program",
                "Carbon offset project",
            ],
            "Title": [
                "Community-based solar power project",
                "Afforestation and reforestation program",
                "Organic farming and soil conservation project",
                "Mangrove restoration and conservation project",
            ],
            "FP number": ["CCP001", "REI002", "SAP003", "COP004"],
            "Organisation": [
                "Global Climate Alliance",
                "Renewable Energy Solutions",
                "Green Agriculture Foundation",
                "Carbon Neutral Group",
            ],
            "Country": ["Global", "International", "Earth", "Planet"],
            "Topic": [
                "Solar Energy",
                "Forest Conservation",
                "Sustainable Farming",
                "Ecosystem Restoration",
            ],
            "Main file (English)": [
                "https://www.climateprojects.org/solar-power-project.pdf",
                "https://www.climateprojects.org/reforestation-program.pdf",
                "https://www.climateprojects.org/organic-farming-project.pdf",
                "https://www.climateprojects.org/mangrove-conservation-project.pdf",
            ],
            "Translated languages": [pd.NA for _ in range(4)],
            "Translated titles": [pd.NA for _ in range(4)],
            "Translated files": [pd.NA for _ in range(4)],
            "Document page permalink": [
                "https://www.climateprojects.org/solar-power-project",
                "https://www.climateprojects.org/reforestation-program",
                "https://www.climateprojects.org/organic-farming-project",
                "https://www.climateprojects.org/mangrove-conservation-project",
            ],
            "Cover date": ["2022-01-01", "2022-02-01", "2022-03-01", "2022-04-01"],
            "Updated date (UTC)": [
                "2022-01-15 08:00:00",
                "2022-02-15 10:00:00",
                "2022-03-15 12:00:00",
                "2022-04-15 14:00:00",
            ],
            "Summary": [
                "This document presents a climate change mitigation project focusing on community-based solar power generation.",
                "This document presents a renewable energy initiative for afforestation and reforestation.",
                "This document presents a sustainable agriculture program emphasizing organic farming and soil conservation.",
                "This document presents a carbon offset project for mangrove restoration and conservation.",
            ],
        }
    )


@pytest.fixture()
def test_document_df_with_translated_docs():
    yield pd.DataFrame(
        {
            "ID": [1001, 1002, 1003],
            "Type": [
                "Climate Action Plans",
                "Climate Action Plans",
                "Climate Action Plans",
            ],
            "Title": [
                "Strategies for Accelerating Renewable Energy Adoption",
                "Principles and Guidelines for Sustainable Urban Development",
                "Framework for Climate Resilience and Adaptation",
            ],
            "FP number": ["", "", ""],
            "Organisation": [
                "Green Energy Initiative",
                "Urban Sustainability Coalition",
                "Climate Adaptation Network",
            ],
            "Main file (English)": [
                "https://www.climateprojects.org/docs/renewable-energy-strategies.pdf",
                "https://www.climateprojects.org/docs/sustainable-urban-development.pdf",
                "https://www.climateprojects.org/docs/climate-resilience-framework.pdf",
            ],
            "Translated languages": [
                "العربية|Español|Français|Русский|中文",
                "العربية|Español|Français|Русский|中文",
                pd.NA,
            ],
            "Translated titles": [
                "استراتيجيات تسريع تبني الطاقة المتجددة|Estrategias para acelerar la adopción de energías renovables|Stratégies pour accélérer l'adoption des énergies renouvelables|Стратегии по ускорению внедрения возобновляемых источников энергии|加速采用可再生能源的策略",
                "مبادئ وإرشادات التنمية الحضرية المستدامة|Principios y directrices para el desarrollo urbano sostenible|Principes et directives pour le développement urbain durable|Принципы и рекомендации для устойчивого городского развития|可持续城市发展的原则和指南",
                pd.NA,
            ],
            "Translated files": [
                "https://www.climateprojects.org/docs/ar-renewable-energy-strategies.pdf|https://www.climateprojects.org/docs/es-renewable-energy-strategies.pdf|https://www.climateprojects.org/docs/fr-renewable-energy-strategies.pdf|https://www.climate_projects.org/docs/ru-renewable-energy-strategies.pdf|https://www.climateprojects.org/docs/zh-renewable-energy-strategies.pdf",
                "https://www.climateprojects.org/docs/ar-sustainable-urban-development.pdf|https://www.climateprojects.org/docs/es-sustainable-urban-development.pdf|https://www.climateprojects.org/docs/fr-sustainable-urban-development.pdf|https://www.climate_projects.org/docs/ru-sustainable-urban-development.pdf|https://www.climateprojects.org/docs/zh-sustainable-urban-development.pdf",
                pd.NA,
            ],
            "Document page permalink": [
                "https://www.climateprojects.org/document/renewable-energy-strategies",
                "https://www.climateprojects.org/document/sustainable-urban-development",
                "https://www.climateprojects.org/document/climate-resilience-framework",
            ],
            "Cover date": ["2023-01-15", "2022-11-10", "2024-03-22"],
            "Updated date (UTC)": [
                "2023-06-15 12:30:00",
                "2023-06-10 11:00:00",
                "2024-03-22 09:15:00",
            ],
            "Summary": [
                "Outlines strategies for accelerating the adoption of renewable energy technologies to reduce carbon emissions and promote sustainability.",
                "Provides principles and guidelines for integrating sustainability into urban development projects to enhance environmental and social outcomes.",
                "Describes a framework for improving climate resilience and adaptation measures to address the impacts of climate change on vulnerable communities.",
            ],
        }
    )


@pytest.fixture()
def test_document_df_with_invalid_urls():
    yield pd.DataFrame(
        {
            "ID": [6617],
            "Type": ["Policies, strategies, and guidelines"],
            "Title": [
                "Guidelines for enhanced country ownership and country drivenness"
            ],
            "FP number": [""],
            "Organisation": ["Country ownership"],
            "Main file (English)": [
                "https://www.mocksite.com/sites/default/files/document/guidelines-enhanced-country-ownership-country-drivenness.pdf"
            ],
            "Translated languages": ["العربية|Español|Français|Русский|中文"],
            "Translated titles": [
                "تغير المناخ|Cambio climático|Changement climatique|Изменение климата|气候变化"
            ],
            "Translated files": [
                "https://www.mocksite.com/sites/default/files/document/this^is^invalid/ar-guidelines-enhanced-country-ownership-country-drivenness.pdf|https://www.mocksite.com/sites/default/files/document/es-guidelines-enhanced-country-ownership-country-drivenness.pdf|https://www.mocksite.com/sites/default/files/document/fr-guidelines-enhanced-country-ownership-country-drivenness.pdf|https://www.mocksite.com/sites/default/files/document/zh-guidelines-enhanced-country-ownership-country-drivenness.pdf"
            ],
            "Document page permalink": [
                "https://www.mocksite.com/document/guidelines-enhanced-country-ownership-and-country-drivenness"
            ],
            "Cover date": ["2017-07-06"],
            "Updated date (UTC)": ["2022-12-01 02:16:43"],
            "Summary": [
                "Adopted by decision [decision:B.17/21]. Sets out guidelines for enhanced country ownership and country drivenness, covering guiding principles, role of country programmes and structured dialogues, role of country ownership in the Fund's operating modalities, and evaluation."
            ],
        }
    )


@pytest.fixture()
def test_document_df_with_duplicate_urls():
    yield pd.DataFrame(
        {
            "ID": [6618],
            "Type": ["Policies, strategies, and guidelines"],
            "Title": [
                "Guidelines for enhanced country ownership and country drivenness"
            ],
            "FP number": [""],
            "Organisation": ["Country ownership"],
            "Main file (English)": ["https://www.mocksite.com/mockfile.pdf"],
            "Translated languages": ["العربية|Español|Français|Русский|中文"],
            "Translated titles": [
                "تغير المناخ|Cambio climático|Changement climatique|Изменение климата|气候变化"
            ],
            "Translated files": [
                "https://www.mocksite.com/ar-file.pdf|https://www.mocksite.com/es-file.pdf|https://www.mocksite.com/fr-file.pdf|https://www.mocksite.com/zh-file.pdf|https://www.mocksite.com/zh-file.pdf"  # Empty URL
            ],
            "Document page permalink": ["https://www.mocksite.com/mockdocument"],
            "Cover date": ["2017-07-06"],
            "Updated date (UTC)": ["2022-12-01 02:16:43"],
            "Summary": [
                "Adopted by decision [decision:B.17/21]. Sets out guidelines for enhanced country ownership and country drivenness, covering guiding principles, role of country programmes and structured dialogues, role of country ownership in the Fund's operating modalities, and evaluation."
            ],
        }
    )


@pytest.fixture()
def test_document_df_with_empty_url():
    yield pd.DataFrame(
        {
            "ID": [6617],
            "Type": ["Policies, strategies, and guidelines"],
            "Title": [
                "Guidelines for enhanced country ownership and country drivenness"
            ],
            "FP number": [""],
            "Organisation": ["Country ownership"],
            "Main file (English)": ["https://www.mocksite.com/mockfile.pdf"],
            "Translated languages": ["العربية|Español|Français|Русский|中文"],
            "Translated titles": [
                "تغير المناخ|Cambio climático|Changement climatique|Изменение климата|气候变化"
            ],
            "Translated files": [
                "https://www.mocksite.com/ar-file.pdf|https://www.mocksite.com/es-file.pdf|https://www.mocksite.com/fr-file.pdf||https://www.mocksite.com/zh-file.pdf"  # Empty URL
            ],
            "Document page permalink": ["https://www.mocksite.com/mockdocument"],
            "Cover date": ["2017-07-06"],
            "Updated date (UTC)": ["2022-12-01 02:16:43"],
            "Summary": [
                "Adopted by decision [decision:B.17/21]. Sets out guidelines for enhanced country ownership and country drivenness, covering guiding principles, role of country programmes and structured dialogues, role of country ownership in the Fund's operating modalities, and evaluation."
            ],
        }
    )
