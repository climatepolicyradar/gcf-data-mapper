from typing import Any, Optional

import click
import pandas as pd

from gcf_data_mapper.enums.family import (
    FamilyColumnsNames,
    FamilyNestedColumnNames,
    GCFProjectBudgetSource,
)
from gcf_data_mapper.parsers.helpers import (
    arrays_contain_empty_values,
    row_contains_columns_with_empty_values,
    verify_required_fields_present,
)


def get_budgets(funding_list: list[dict], source: str) -> list[int]:
    """Get the budget amount from the row based on the funding source.

    :param list[dict] row: A list of all the funding information, represented in dictionaries
    :param str source: The funding source to retrieve the budget from.

    :return list[int]: A list of budget amounts corresponding to the source,
        or [0] if the source is not found.
    """

    budget_key = FamilyNestedColumnNames.BUDGET.value
    source_key = FamilyNestedColumnNames.SOURCE.value

    budgets = [
        funding[budget_key] for funding in funding_list if funding[source_key] == source
    ]

    # Where we have projects which have been solely funded by the fund (GCF), or solely co-financed
    # - so in instances where there will be no funding that match either the GCF or co-financing
    # source value, we will map the `project_value_fund spend` or the `project_value_co_financing`
    # as an array with 0 i.e [0]
    return budgets if budgets else [0]


def map_family_metadata(row: pd.Series) -> Optional[dict]:
    """Map the metadata of a family based on the provided row.

    :param pd.Series row: The row containing family information.
    :return Optional[dict]: A dictionary containing mapped metadata for the family.
    """

    countries = row.at[FamilyColumnsNames.COUNTRIES.value]
    entities = row.at[FamilyColumnsNames.ENTITIES.value]
    funding_sources = row.at[FamilyColumnsNames.FUNDING.value]
    result_areas = row.at[FamilyColumnsNames.RESULT_AREAS.value]

    area_key = FamilyNestedColumnNames.AREA.value
    name_key = FamilyNestedColumnNames.NAME.value
    region_key = FamilyNestedColumnNames.REGION.value
    type_key = FamilyNestedColumnNames.TYPE.value

    co_financing_budgets = get_budgets(
        funding_sources, GCFProjectBudgetSource.CO_FINANCING.value
    )
    gcf_budgets = get_budgets(funding_sources, GCFProjectBudgetSource.GCF.value)

    implementing_agencies = [entity[name_key] for entity in entities]
    regions = [country[region_key] for country in countries]
    areas = [result[area_key] for result in result_areas]
    types = [result[type_key] for result in result_areas]

    # As we are filtering the budget information by source for gcf and co financing, we
    # know there will be instances where only one type of funding exists so checking
    # for empty/false values would create false positives, hence the exclusion from this
    # check
    if arrays_contain_empty_values(
        [
            ("Implementing Agencies", implementing_agencies),
            ("Regions", regions),
            ("Result Areas", areas),
            ("Result Types", types),
        ],
        row.at[FamilyColumnsNames.PROJECTS_ID.value],
    ):
        return None

    metadata = {
        "approved_ref": [row.at[FamilyColumnsNames.APPROVED_REF.value]],
        "implementing_agencies": list(set(implementing_agencies)),
        "project_id": [row.at[FamilyColumnsNames.PROJECTS_ID.value]],
        "project_url": [row.at[FamilyColumnsNames.PROJECT_URL.value]],
        "project_value_fund_spend": gcf_budgets,
        "project_value_co_financing": co_financing_budgets,
        "regions": list(set(regions)),
        "result_areas": list(set(areas)),
        "result_types": list(set(types)),
        "sector": [row.at[FamilyColumnsNames.SECTOR.value]],
        "theme": [row.at[FamilyColumnsNames.THEME.value]],
    }

    return metadata


def map_family_data(
    row: pd.Series,
) -> Optional[dict]:
    """Map the data of a family based on the provided row.

    :param pd.Series row: The containing family and family metadata information.
    :return Optional[dict]: A dictionary containing the mapped family data.
    """

    family_metadata = map_family_metadata(row)

    # When processing the family metadata if there are any empty/falsy values we return None
    # and skip the row. Therefore we don't want to process the rest of the family data so we
    # return None in this conditional.
    if family_metadata is None:
        click.echo("🛑 Skipping row as family metadata has missing information")
        return None

    approved_ref = row.at[FamilyColumnsNames.APPROVED_REF.value]
    projects_id = row.at[FamilyColumnsNames.PROJECTS_ID.value]
    summary = row.at[FamilyColumnsNames.SUMMARY.value]
    title = row.at[FamilyColumnsNames.TITLE.value]

    geographies = [
        country[FamilyNestedColumnNames.COUNTRY_ISO3.value]
        for country in row.at[FamilyColumnsNames.COUNTRIES.value]
    ]

    import_id = f"GCF.family.{approved_ref}.{projects_id}"

    family_data = {
        # For now we are hard coding the category as MCF
        "category": "MCF",
        "description": summary,
        "geographies": geographies,
        "import_id": import_id,
        "metadata": family_metadata,
        "title": title,
    }

    return family_data


def process_row(
    row: pd.Series,
    projects_id: str,
    required_columns: list[str],
) -> Optional[dict]:
    """Map the family data based on the provided row.

    :param pd.Series row: The row containing family information.
    :param str projects_id: The id of the current project that is being reformatted/processed
    :param list required_columns: The list of required columns that we need to extract the
        data from in the project
    :return Optional[dict]: A dictionary containing mapped data for the family entity.
        The function will return None, if the row contains missing data from expected columns/fields
    """

    if pd.isna(projects_id) or bool(projects_id) is False:
        click.echo("🛑 Skipping row as it does not contain a project id")
        return None

    if row_contains_columns_with_empty_values(row, required_columns):
        click.echo(
            f"🛑 Skipping row as it contains empty column values: See Project ID {projects_id}"
        )
        return None

    return map_family_data(row)


def family(
    gcf_projects_data: pd.DataFrame, debug: bool
) -> list[Optional[dict[str, Any]]]:
    """Map the GCF family info to new structure.

    :param pd.DataFrame projects_data: The MCF and GCF project data,
        joined on FP num.
    :param bool debug: Whether debug mode is on.
    :return list[Optional[dict[str, Any]]]: A list of GCF families in
        the 'destination' format described in the GCF Data Mapper Google
        Sheet.
    """

    if debug:
        click.echo("📝 Wrangling GCF family data.")

    mapped_families = []

    required_fields = set(str(e.value) for e in FamilyColumnsNames)

    verify_required_fields_present(gcf_projects_data, required_fields)
    # Do a check that the projects data has the field you need

    for _, row in gcf_projects_data.iterrows():
        projects_id = row.at[FamilyColumnsNames.PROJECTS_ID.value]
        mapped_families.append(process_row(row, projects_id, list(required_fields)))

    return mapped_families
