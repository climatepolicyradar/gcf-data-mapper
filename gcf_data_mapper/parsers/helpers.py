from typing import Any

import click
import pandas as pd


def verify_required_fields_present(
    data: pd.DataFrame, required_fields: set[str]
) -> bool:
    """Map the GCF event info to new structure.

    :param pd.DataFrame data: The DataFrame to check.
    :param set[str] required_fields: The required DataFrame columns.
    :raise AttributeError if any of the required fields are missing.
    :return bool: True if the DataFrame contains the required fields.
    """
    cols = set(data.columns)
    diff = set(required_fields).difference(cols)
    if diff == set():
        return True

    raise AttributeError(
        f"Required fields '{str(diff)}' not present in df columns '"
        f"{cols if cols != set() else r'{}'}'"
    )


def check_required_column_value_not_na(row: pd.Series, column_enum) -> bool:
    """Check if the row contains valid document column values (not NA)."""
    return all(pd.notna(row[column.value]) for column in column_enum)


def row_contains_columns_with_empty_values(
    row: pd.Series, required_columns: list[str]
) -> bool:
    """Check that all required values in the given row are not empty (isna).

    :param pd.Series row: The row to check for isna values.
    :param list[str] required_columns: A list of column names that will be used to verify
    isna values.
    :return bool: True if the row contains columns with empty values, false if if all
    expected columns are populated
    """

    # Ensure we are working with a pandas Series by re-selecting the required columns as a Series
    row_subset = pd.Series(row[required_columns], index=required_columns)

    if row_subset.isna().any():
        return True
    return False


def check_row_for_missing_columns(
    row: pd.Series, required_columns: list[str], id_identifier: str
):
    """Check if a given row contains all required columns.

    :param pd.Series row: The row (Series) to check for missing columns.
    :param list[str] required_columns: A list of column names.
    :param str id_identifier: This is the id (i.e project id) of the offending row, this should
    make it easier to debug where and why the tool has errored
    :raises AttributeError: If any required columns are missing from the row.
    """

    missing_columns = set(required_columns).difference(set(row.index))

    if missing_columns:
        raise AttributeError(
            f"The data series at id {id_identifier} is missing these required columns: {', '.join(sorted(missing_columns))}"
        )


# This checks that a key value pair exists on a nested dictionary, we want to be strict
# with our validation so want to be alerted when data that we expect to be there does
# not exist, we can then take this back to the client and handle it accordingly
def get_value_in_nested_object(object: dict, key: str) -> Any:
    """Retrieve the value associated with a given key in a nested dictionary object.

    :param dict object: The dictionary from which to retrieve the value.
    :param str key: The key value that will be used to retrieve that value.
    :param str id_identifier: This is the id (i.e project id) of the offending row, this should
    make it easier to debug where we have missing data

    :raises KeyError: If the specified key does not exist in the dictionary.

    :return Any: The value associated with the specified key.
    """

    # The get function, checks for a key in a dict and defaults to None instead of
    # raising a key error. However for null values in a json object this converts to a NoneType,
    # so to avoid false positives, we set the default to a specified string so that we
    # can know for sure when a value is empty vs when a key does not exists
    value = object.get(key, "key does not exist")

    if value == "key does not exist":
        raise KeyError(f"key: '{key}' does not exist on this dict")

    # Check for false values like empty string, empty list, or empty dict or None
    if not value:
        click.echo(f"🛑 Key '{key}' exists, but the value is empty")

    return value
