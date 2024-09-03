from enum import Enum
from typing import Any, Optional

import click
import pandas as pd

from gcf_data_mapper.parsers.helpers import verify_required_fields_present


class RequiredColumns(Enum):
    APPROVED = "ApprovalDate"
    UNDER_IMPLEMENTATION = "StartDate"
    COMPLETED = "DateCompletion"


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
    verify_required_fields_present(projects_data, required_fields)

    return []
