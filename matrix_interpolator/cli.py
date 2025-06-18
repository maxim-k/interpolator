import logging
import sys

import click

from . import core, io
from .exceptions import InvalidMatrixError, SuspiciousGapsError

# Configure root logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@click.command()
@click.argument("input_csv", type=click.Path(exists=True, dir_okay=False))
@click.argument("output_csv", type=click.Path(writable=True))
@click.option(
    "--passes",
    "-p",
    default=1,
    show_default=True,
    help="Number of interpolation passes",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging")
def main(input_csv: str, output_csv: str, passes: int, verbose: bool) -> None:
    """
    Command-line tool: interpolate missing values in a CSV matrix.

    CLI entry-point using Click. Reads INPUT_CSV, performs interpolation,
    and writes to OUTPUT_CSV.

    :param input_csv: Path to source CSV file.
    :param output_csv: Path for result CSV file.
    :param passes: How many passes of interpolation to run.
    :param verbose: If set, enable DEBUG-level logging.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    try:
        logger.debug("Reading matrix from %s", input_csv)
        matrix = io.read_matrix(input_csv)

        logger.debug("Starting interpolation with %d passes", passes)
        filled = core.interpolate(matrix, passes=passes)

        logger.debug("Writing interpolated matrix to %s", output_csv)
        io.write_matrix(filled, output_csv)

        logger.info("Interpolation complete.")
    except (InvalidMatrixError, SuspiciousGapsError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
