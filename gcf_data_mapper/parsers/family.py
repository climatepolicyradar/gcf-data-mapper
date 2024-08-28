from typing import Any, Optional

import click
import pandas as pd


def family(projects_data: pd.DataFrame, debug: bool) -> list[Optional[dict[str, Any]]]:
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

    return []
