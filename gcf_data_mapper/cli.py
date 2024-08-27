import click


@click.command()
@click.option("--name", required=True, help="The name to greet.")
@click.version_option("0.1.0", "--version", "-v", help="Show the version and exit.")
def greet(name):
    """Simple program that greets NAME."""
    click.echo(f"Hello {name}!")


if __name__ == "__main__":
    greet()
