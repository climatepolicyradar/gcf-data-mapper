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

    # sets are naturally un-ordered, sorting them means we can test the error message reliably
    sorted_diff = sorted(diff)
    sorted_cols = sorted(cols)

    raise AttributeError(
        f"Required fields {sorted_diff} not present in df columns {sorted_cols}"
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


def arrays_contain_empty_values(list_values: list[tuple], id: str) -> bool:
    """Checks the list in a tuple for empty (falsy) values; {}, [], None, ''

    :param list[tuple] list_values: A list of tuples containing the name and array of values
    :param str id: The ID of the project to include in message that we echo to the terminal.
    :return bool: True if any list contains empty values, False otherwise.
    """
    arrays_with_empty_values = [
        name for name, array in list_values if any(not value for value in array)
    ]

    if arrays_with_empty_values:
        click.echo(
            f"🛑 The following lists contain empty values: {', '.join(sorted(arrays_with_empty_values))}. Projects ID {id}"
        )
        return True

    return False
