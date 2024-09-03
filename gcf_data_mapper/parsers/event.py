from enum import Enum
from typing import Any, Optional

import click
import pandas as pd


class RequiredColumns(Enum):
    APPROVED = "ApprovalDate"
    UNDER_IMPLEMENTATION = "StartDate"
    COMPLETED = "DateCompletion"


def has_required_fields(
    data: pd.DataFrame, required_fields: set[str], debug: bool = False
) -> bool:
    """Map the GCF event info to new structure.

    :param pd.DataFrame data: The DataFrame to check.
    :param set[str] required_fields: The required DataFrame columns.
    :param bool debug: Whether debug mode is on.
    :return bool: True if the DataFrame contains the required fields,
        otherwise False.
    """
    diff = set(required_fields).difference(set(data.columns))
    if diff == set():
        return True

    if debug:
        click.echo(f"❌ Required fields '{diff}' not present in {set(data.columns)}")
    return False


def event(projects_data: pd.DataFrame, debug: bool) -> list[Optional[dict[str, Any]]]:
    """Map the GCF event info to new structure.

    :param pd.DataFrame projects_data: The MCF and GCF project data,
        joined on FP num.
    :param bool debug: Whether debug mode is on.
    :return list[Optional[dict[str, Any]]]: A list of GCF families in
        the 'destination' format described in the GCF Data Mapper Google
        Sheet.
    """
    if debug:
        click.echo("📝 Wrangling GCF event data.")

    required_fields = set(str(e.value) for e in RequiredColumns)
    if not has_required_fields(projects_data, required_fields):
        return []

    return []
