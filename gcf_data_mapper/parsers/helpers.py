import click
import pandas as pd


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
