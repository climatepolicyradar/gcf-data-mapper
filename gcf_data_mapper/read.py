import json
import os
from enum import Enum
from typing import Optional, Union

import click
import pandas as pd


class AllowedFileExtensions(Enum):
    JSON = "json"
    CSV = "csv"


def read_csv_pd(
    file_path: str,
    header_rows: Optional[Union[int, list[int]]] = 0,
    chunk_size: int = 10**4,
) -> pd.DataFrame:
    """Load the data from the specified CSV file into a Pandas DF.

    :param str file_path: The filepath passed by the user to the
        tool.
    :param Optional[Union[int, list[int]]] header_rows: The indexes of
        any rows in the file that contain headers. Defaults to 0 (which
        is the first line of the file), but can also be None if no
        header rows exist or an array of indexes if multiple rows
        contain headers.
    :param Optional[int] chunk_size: The number of lines to read into
        memory in each batch iteratively. Defaults to 10**4.

    :return pd.DataFrame: A Pandas DataFrame containing the CSV data if
        the file is successfully found and parsed by the Pandas CSV
        reader. Otherwise an empty DataFrame will be returned.
    """
    # Should the path exist, read the CSV contents into memory iteratively in chunks of
    # 'chunk_size' (10**4 by default).
    # This helps prevent out of memory errors where there is insufficient memory to
    # handling reading in the file contents e.g., when handling super large datasets.
    try:
        # By using 'chunksize' we create a list of chunks (each chunk being a DataFrame
        # containing 'chunk_size' lines of the original file).
        all_chunks = pd.read_csv(
            file_path, chunksize=chunk_size, header=header_rows, encoding="utf-8"
        )

        # We can then concatenate each of the chunks into a single dataframe, thus
        # reducing complexity.
        dataset = pd.concat(all_chunks)
        return dataset

    except Exception as e:
        click.echo(f"❌ Error reading file {file_path}: {e}")

    return pd.DataFrame([])


def read_json_pd(file_path: str) -> pd.DataFrame:
    """Load the data from the specified JSON file into a Pandas DF.

    :param str file_path: The filepath passed by the user to the
        tool.

    :return pd.DataFrame: A Pandas DataFrame containing the CSV data if
        the file is successfully found and parsed by the Pandas CSV
        reader. Otherwise an empty DataFrame will be returned.
    """
    try:
        with open(file_path, "r") as file:
            df = pd.json_normalize(json.load(file))
        return df
    except Exception as e:
        click.echo(f"❌ Error reading file {file_path}: {e}")
    return pd.DataFrame([])


def read_into_pandas(file_path: str, debug: bool = False) -> pd.DataFrame:
    """Read a CSV or JSON file into a Pandas dataframe.

    Simple program that validates a file path for existence, type and
    emptiness, which then calls a function to read the file into Pandas
    based on its file type.

    :param file_path str: A file path to the csv/json file
    :param bool debug: Whether debug mode is on.
    :raises ValueError: if a non csv or json file type is provided
    :raises FileNotFoundError: if the file does not exist
    :raises ValueError: if the file is empty
    :return Optional[Union[dict[str, Any], list[dict[str, Any]]]]: A
        dictionary or list of dictionaries
    depending on the file type
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file or directory: '{file_path}'")

    file_extension = os.path.splitext(file_path)[1][1:]
    if file_extension not in [e.value for e in AllowedFileExtensions]:
        raise ValueError("Error reading file: File must be a valid json or csv file")

    if os.path.getsize(file_path) == 0 and debug:
        click.echo(f"File '{file_path}' is empty")

    df = pd.DataFrame([])

    if file_extension == AllowedFileExtensions.CSV.value:
        df = read_csv_pd(file_path)

    elif file_extension == AllowedFileExtensions.JSON.value:
        df = read_json_pd(file_path)

    return df


def read(
    gcf_projects_file: str,
    mcf_projects_file: str,
    mcf_docs_file: str,
    debug: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Put the mapped GCF data into a dictionary ready for dumping.

    The output of this function will get dumped as JSON to the output
    file.

    :param str gcf_projects_file: The GCF projects filename.
    :param str mcf_projects_file: The MCF projects filename.
    :param str mcf_docs_file: The MCF projects filename.
    :param bool debug: Whether debug mode is on.
    :return dict[str, list[Optional[dict[str, Any]]]]: The GCF data
        mapped to the Document-Family-Collection-Event entity it
        corresponds to.
    """
    gcf_projects: pd.DataFrame = read_into_pandas(gcf_projects_file, debug)
    mcf_projects: pd.DataFrame = read_into_pandas(mcf_projects_file, debug)
    mcf_docs: pd.DataFrame = read_into_pandas(mcf_docs_file, debug)

    if any(
        data is None or data.empty for data in [gcf_projects, mcf_projects, mcf_docs]
    ):
        raise ValueError("One or more of the expected dataframes are empty")

    # Join the MCF and GCF project data by the 'FP number' a.k.a ApprovedRef.
    if gcf_projects.shape[0] != mcf_projects.shape[0]:
        click.echo(
            f"❌ GCF project data {gcf_projects.shape[0]}, MCF project data {mcf_projects.shape[0]}"
        )
        raise ValueError("Record number mismatch")

    if debug:
        click.echo("📝 Merging GCF and MCF project data")
    mcf_projects.rename(columns={"FP number": "ApprovedRef"}, inplace=True)
    project_info = pd.merge(
        left=gcf_projects,
        right=mcf_projects,
    )

    if debug:
        click.echo(project_info)
        click.echo(mcf_docs)

    return project_info, mcf_docs
