import click


@click.group()
def cli():
    pass


@click.command("read_data_file")
@click.argument("file_path", type=click.Path(exists=True))
def read_data_file(file_path: str):
    """Read the data file"""
    click.echo("Read Data File")


def entrypoint():
    # trunk-ignore(pyright/reportFunctionMemberAccess)
    cli.add_command(read_data_file)
    cli()


if __name__ == "__main__":
    entrypoint()
