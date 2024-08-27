import csv
import json

import click


def read_csv(file_path: str) -> list[str]:
    """Reads a csv file and returns a list of values"""
    with open(file_path, "r") as file:
        csv_reader = csv.DictReader(file)
        data = []
        for line in csv_reader:
            data.append(line["country"])
        return data


def read_json(file_path: str):
    """Reads a json file, we will just read the file for now and echo a value"""
    with open(file_path, "r") as file:
        data = file.read()
        return json.loads(data)


def read_data_file(file_path: str):
    """Simple program that reads a data file, calls a function to read a csv or json file respectively"""
    file_extension = file_path.lower().split(".")[-1]
    if file_extension not in ["json", "csv"]:
        raise ValueError("Error reading file: File must be a valid json or csv file")
    try:
        if file_extension == "csv":
            return read_csv(file_path)
        elif file_extension == "json":
            return read_json(file_path)
    except Exception as e:
        click.echo(f"Error reading file: {e}")
