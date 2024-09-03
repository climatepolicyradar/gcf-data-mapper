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
            "ID": [5539, 5540, 5541, 5542],
            "Type": [
                "Approved funding proposal",
                "Approved funding proposal",
                "Approved funding proposal",
                "Approved funding proposal",
            ],
            "Title": [
                "Enhancing climate resilience of the water sector in Bahrain",
                "Nigeria solar IPP support programme",
                "Sustainable urban development in Kenya",
                "Renewable energy initiatives in India",
            ],
            "FP number": ["SAP003", "FP104", "FP105", "FP106"],
            "Organisation": [
                "United Nations Environment Programme",
                "Africa Finance Corporation",
                "World Bank",
                "Asian Development Bank",
            ],
            "Country": ["Bahrain", "Nigeria", "Kenya", "India"],
            "Topic": ["", "", "", ""],
            "Main file (English)": [
                "https://www.greenclimate.fund/sites/default/files/document/funding-proposal-sap003-unep-bahrain.pdf",
                "https://www.greenclimate.fund/sites/default/files/document/funding-proposal-fp104-afc-nigeria.pdf",
                "https://www.greenclimate.fund/sites/default/files/document/funding-proposal-fp105-world-bank-kenya.pdf",
                "https://www.greenclimate.fund/sites/default/files/document/funding-proposal-fp106-adb-india.pdf",
            ],
            "Translated languages": [pd.NA for _ in range(4)],
            "Translated titles": [pd.NA for _ in range(4)],
            "Translated files": [pd.NA for _ in range(4)],
            "Document page permalink": [
                "https://www.greenclimate.fund/document/enhancing-climate-resilience-water-sector-bahrain",
                "https://www.greenclimate.fund/document/nigeria-solar-ipp-support-programme",
                "https://www.greenclimate.fund/document/sustainable-urban-development-kenya",
                "https://www.greenclimate.fund/document/renewable-energy-initiatives-india",
            ],
            "Cover date": ["2018-12-22", "2019-03-21", "2020-05-15", "2021-08-10"],
            "Updated date (UTC)": [
                "2019-07-30 05:38:06",
                "2019-07-30 05:41:06",
                "2020-06-01 10:00:00",
                "2021-09-15 12:30:00",
            ],
            "Summary": [
                'This document presents funding proposal "SAP003: Enhancing climate resilience of the water sector in Bahrain," as approved by the Board of the Green Climate Fund at B.21.',
                'This document presents funding proposal "FP0104: Nigeria solar IPP support programme," as approved by the Board of the Green Climate Fund at B.22.',
                'This document presents funding proposal "FP0105: Sustainable urban development in Kenya," as approved by the Board of the Green Climate Fund at B.23.',
                'This document presents funding proposal "FP0106: Renewable energy initiatives in India," as approved by the Board of the Green Climate Fund at B.24.',
            ],
        }
    )


@pytest.fixture()
def test_document_df_with_translated_docs():
    yield pd.DataFrame(
        {
            "ID": [6614, 6615, 6616],
            "Type": [
                "Policies, strategies, and guidelines",
                "Policies, strategies, and guidelines",
                "Policies, strategies, and guidelines",
            ],
            "Title": [
                "Guidelines for enhanced country ownership and country drivenness",
                "General principles and indicative list of eligible costs covered under GCF fees and project management costs",
                "Framework for climate finance and investment strategies",
            ],
            "FP number": ["", "", ""],  # Assuming FP number is empty
            "Organisation": [
                "Country ownership",
                "Accreditation",
                "Climate Finance Unit",
            ],
            "Main file (English)": [
                "https://www.greenclimate.fund/sites/default/files/document/guidelines-enhanced-country-ownership-country-drivenness.pdf",
                "https://www.greenclimate.fund/sites/default/files/document/principles-list-costs-pm.pdf",
                "https://www.greenclimate.fund/sites/default/files/document/climate-finance-investment-strategies.pdf",
            ],
            "Translated languages": [
                "العربية|Español|Français|Русский|中文",
                "العربية|Español|Français|Русский|中文",
                pd.NA,
            ],
            "Translated titles": [
                "المبادئ التوجيهية للملكية الق ُ طرية والتوجه الق طري|Directrices para aumentar la implicación nacional y el impulso de los países|Lignes directrices pour une meilleure appropriation et un plus grand pilotage par les pays|Руководящие принципы повышения ответственности и инициативности стран|国家自主权和国家驱动力加强准则",
                "قائمة المبادئ العامة والرشادية للتكاليف المستوفاة الشروط المغطاة بموجب رسوم الصندوق الأخضر للمناخ ‏‪ GCF‬وتكاليف إدارة المشاريع |Principios generales y lista orientativa de gastos que podrían estar cubiertos en las comisiones y gastos de gestión de proyectos del GCF|Principes généraux et liste indicative des coûts admissibles au titre des honoraires et des frais de gestion des projets du GCF|Общие принципы и ориентировочный перечень приемлемых расходов, покрываемых за счет комиссионных выплат фонда GCF и расходов на управление проектами|一般原则以及GCF费用和项目管理费用所涵盖的合格费用的指示性清单",
                pd.NA,
            ],
            "Translated files": [
                "https://www.greenclimate.fund/sites/default/files/document/ar-guidelines-enhanced-country-ownership-country-drivenness.pdf|https://www.greenclimate.fund/sites/default/files/document/es-guidelines-enhanced-country-ownership-country-drivenness.pdf|https://www.greenclimate.fund/sites/default/files/document/fr-guidelines-enhanced-country-ownership-country-drivenness.pdf|https://www.greenclimate.fund/sites/default/files/document/ru-guidelines-enhanced-country-ownership-country-drivenns.pdf|https://www.greenclimate.fund/sites/default/files/document/zh-guidelines-enhanced-country-ownership-country-drivenns.pdf",
                "https://www.greenclimate.fund/sites/default/files/document/ar-principles-list-costs-pm_0.pdf|https://www.greenclimate.fund/sites/default/files/document/es-principles-list-costs-pm.pdf|https://www.greenclimate.fund/sites/default/files/document/fr-principles-list-costs-pm.pdf|https://www.greenclimate.fund/sites/default/files/document/ru-principles-list-costs-pm.pdf|https://www.greenclimate.fund/sites/default/files/document/zh-principles-list-costs-pm.pdf",
                pd.NA,
            ],
            "Document page permalink": [
                "https://www.greenclimate.fund/document/guidelines-enhanced-country-ownership-and-country-drivenness",
                "https://www.greenclimate.fund/document/general-principles-and-indicative-list-eligible-costs-covered-under-gcf-fees-and-project",
                "https://www.greenclimate.fund/document/climate-finance-investment-strategies",
            ],
            "Cover date": ["2017-07-06", "2018-03-01", "2021-05-15"],
            "Updated date (UTC)": [
                "2022-12-01 02:16:43",
                "2022-12-01 01:50:56",
                "2022-12-01 03:00:00",
            ],
            "Summary": [
                "Adopted by decision [decision:B.17/21]. Sets out guidelines for enhanced country ownership and country drivenness, covering guiding principles, role of country programmes and structured dialogues, role of country ownership in the Fund's operating modalities, and evaluation.",
                "Adopted by decision [decision:B.19/09]. Outlines the general principles and an indicative list of eligible costs to be covered under accredited entity fees and project management costs.",
                "Adopted by decision [decision:B.20/15]. Provides a framework for climate finance and investment strategies to enhance the effectiveness of climate actions.",
            ],
        }
    )


@pytest.fixture()
def test_document_df_with_invalid_urls():
    yield pd.DataFrame(
        {
            "ID": [6614],
            "Type": ["Policies, strategies, and guidelines"],
            "Title": [
                "Guidelines for enhanced country ownership and country drivenness"
            ],
            "FP number": [""],  # Assuming FP number is empty
            "Organisation": ["Country ownership"],
            "Main file (English)": [
                "https://www.greenclimate.fund/sites/default/files/document/guidelines-enhanced-country-ownership-country-drivenness.pdf"
            ],
            "Translated languages": ["العربية|Español|Français|Русский|中文"],
            "Translated titles": [
                "المبادئ التوجيهية للملكية الق ُ طرية والتوجه الق طري|Directrices para aumentar la implicación nacional y el impulso de los países|Lignes directrices pour une meilleure appropriation et un plus grand pilotage par les pays|Руководящие принципы повышения ответственности и инициативности стран|国家自主权和国家驱动力加强准则"
            ],
            "Translated files": [
                "htps://www.greenclimate.fund/sites/default/files/document/ar-guidelines-enhanced-country-ownership-country-drivenness.pdf|htps://www.greenclimate.fund/sites/default/files/document/es-guidelines-enhanced-country-ownership-country-drivenness.pdf|https://www.greenclimate.fund/sites/default/files/document/fr-guidelines-enhanced-country-ownership-country-drivenness.pdf|https://www.greenclimatefund/this^is^invalid/sites/default/files/document/ru-guidelines-enhanced-country-ownership-country-drivenness.pdf|https://www.greenclimate.fund/sites/default/files/document/zh-guidelines-enhanced-country-ownership-country-drivenness.pdf"  # Invalid URL introduced
            ],
            "Document page permalink": [
                "https://www.greenclimate.fund/document/guidelines-enhanced-country-ownership-and-country-drivenness"
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
            "Main file (English)": [
                "https://www.greenclimate.fund/sites/default/files/document/guidelines-enhanced-country-ownership-country-drivenness.pdf"
            ],
            "Translated languages": ["العربية|Español|Français|Русский|中文"],
            "Translated titles": [
                "المبادئ التوجيهية للملكية الق ُ طرية والتوجه الق طري|Directrices para aumentar la implicación nacional y el impulso de los países|Lignes directrices pour une meilleure appropriation et un plus grand pilotage par les pays|Руководящие принципы повышения ответственности и инициативности стран|国家自主权和国家驱动力加强准则"
            ],
            "Translated files": [
                "https://www.greenclimate.fund/sites/default/files/document/ar-guidelines-enhanced-country-ownership-country-drivenness.pdf|https://www.greenclimate.fund/sites/default/files/document/es-guidelines-enhanced-country-ownership-country-drivenness.pdf|https://www.greenclimate.fund/sites/default/files/document/fr-guidelines-enhanced-country-ownership-country-drivenness.pdf|https://www.greenclimate.fund/sites/default/files/document/ar-guidelines-enhanced-country-ownership-country-drivenness.pdf|https://www.greenclimate.fund/sites/default/files/document/es-guidelines-enhanced-country-ownership-country-drivenness.pdf"
            ],
            "Document page permalink": [
                "https://www.greenclimate.fund/document/guidelines-enhanced-country-ownership-and-country-drivenness"
            ],
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
            "Main file (English)": [
                "https://www.greenclimate.fund/sites/default/files/document/guidelines-enhanced-country-ownership-country-drivenness.pdf"
            ],
            "Translated languages": ["العربية|Español|Français|Русский|中文"],
            "Translated titles": [
                "المبادئ التوجيهية للملكية الق ُ طرية والتوجه الق طري|Directrices para aumentar la implicación nacional y el impulso de los países|Lignes directrices pour une meilleure appropriation et un plus grand pilotage par les pays|Руководящие принципы повышения ответственности и инициативности стран|国家自主权和国家驱动力加强准则"
            ],
            "Translated files": [
                "https://www.greenclimate.fund/sites/default/files/document/ar-guidelines-enhanced-country-ownership-country-drivenness.pdf|https://www.greenclimate.fund/sites/default/files/document/es-guidelines-enhanced-country-ownership-country-drivenness.pdf|https://www.greenclimate.fund/sites/default/files/document/fr-guidelines-enhanced-country-ownership-country-drivenness.pdf||https://www.greenclimate.fund/sites/default/files/document/zh-guidelines-enhanced-country-ownership-country-drivenness.pdf"  # Empty URL
            ],
            "Document page permalink": [
                "https://www.greenclimate.fund/document/guidelines-enhanced-country-ownership-and-country-drivenness"
            ],
            "Cover date": ["2017-07-06"],
            "Updated date (UTC)": ["2022-12-01 02:16:43"],
            "Summary": [
                "Adopted by decision [decision:B.17/21]. Sets out guidelines for enhanced country ownership and country drivenness, covering guiding principles, role of country programmes and structured dialogues, role of country ownership in the Fund's operating modalities, and evaluation."
            ],
        }
    )
