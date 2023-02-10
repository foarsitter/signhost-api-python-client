"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Signhost Api Python Client."""


if __name__ == "__main__":
    main(prog_name="signhost-api-python-client")  # pragma: no cover
