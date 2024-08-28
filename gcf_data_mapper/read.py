import csv
import json
from typing import Optional, Union

import click
import pandas as pd


def read_csv_pd(
    file_path: str,
    header_rows: Optional[Union[int, list[int]]] = 0,
    chunk_size: int = 10**4,
) -> pd.DataFrame:
    """Load the policies from the specified dataset into a Pandas DataFrame.

    :param str file_path:
        The filepath passed by the user to the programme.
    :param Optional[Union[int, list[int]]] header_rows:
        The indexes of any rows in the file that contain headers. Defaults
        to 0 (which is the first line of the file), but can also be None if
        no header rows exist or an array of indexes if multiple rows
        contain headers.
    :param Optional[int] chunk_size:
        The number of lines to read into memory in each batch iteratively.
        Defaults to 10**4.

    :return Optional[pd.DataFrame]:
        A Pandas DataFrame containing the policy data if the file is
        successfully found and parsed by the Pandas CSV reader. Otherwise
        this function will return None.
    """
    # Should the path exist, read the CSV contents into memory iteratively in chunks of 'chunk_size' (10**4 by default).
    # This helps prevent out of memory errors where there is insufficient memory to handling reading in the file
    # contents e.g., when handling super large datasets.
    try:
        # By using 'chunksize' we create a list of chunks (each chunk being a DataFrame containing 'chunk_size' lines of
        # the original file).
        all_chunks = pd.read_csv(
            file_path, chunksize=chunk_size, header=header_rows, encoding="utf-8"
        )

        # We can then concatenate each of the chunks into a single dataframe, thus reducing complexity.
        dataset = pd.concat(all_chunks)
        # click.echo(dataset)
        return dataset

    except FileExistsError:
        click.echo("Error opening file: %s" % file_path)

    except Exception:
        click.echo("Error occurred reading CSV file using Pandas: %s" % file_path)

    return pd.DataFrame([])


def read_csv(file_path: str):
    """Reads a csv file, we will just read the file for now and echo a value"""
    with open(file_path, "r") as file:
        csv_reader = csv.DictReader(file)
        data = []
        for line in csv_reader:
            data.append(line["country"])
        click.echo(data)


def read_json(file_path: str):
    """Reads a json file, we will just read the file for now and echo a value"""
    with open(file_path, "r") as file:
        data = file.read()
        # data = json.load(file)
        click.echo(data)


def read_json_pd(file_path: str):
    """Reads a json file, we will just read the file for now and echo a value"""
    with open(file_path, "r") as file:
        df = pd.json_normalize(json.load(file))
    # df = pd.read_json(file_path)
    # data = json.load(file)
    # click.echo(df)
    return df


def read_data_file(file_path) -> pd.DataFrame:
    """Simple program that reads a data file, calls a function to read a csv or json file respectively"""
    file_extension = file_path.lower().split(".")[-1]
    if file_extension not in ["json", "csv"]:
        raise ValueError("File must be a valid json or csv file")
    try:
        if file_extension == "csv":
            return read_csv_pd(file_path)
            pass
            # return read_csv(file_path)
        if file_extension == "json":
            return read_json_pd(file_path)
            # return read_json(file_path)
    except Exception as e:
        click.echo(f"Error reading file: {e}")
    return pd.DataFrame([])


def concatenate_data(gcf_projects_file, mcf_projects_file, mcf_docs_file, debug: bool):
    """Put the mapped GCF data into a dictionary ready for dumping.

    The output of this function will get dumped as JSON to the output
    file.

    :param click.Path gcf_projects_file: The GCF projects filename.
    :param click.Path mcf_projects_file: The MCF projects filename.
    :param click.Path mcf_docs_file: The MCF projects filename.
    :param click.Path output_file: The output filename.
    :param bool debug: Whether debug mode is on.
    :return dict[str, list[Optional[dict[str, Any]]]]: The GCF data
        mapped to the Document-Family-Collection-Event entity it
        corresponds to.
    """
    gcf_projects = read_data_file(gcf_projects_file)
    mcf_projects = read_data_file(mcf_projects_file)
    mcf_docs = read_data_file(mcf_docs_file)
    return gcf_projects, mcf_projects, mcf_docs
