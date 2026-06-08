from __future__ import absolute_import

import click

from .mining import mining


@click.command(
    short_help="Search for a smaller secondary inside a larger reference image",
    help="This workflow searches for a smaller secondary image inside a larger reference image using a coarse-to-fine rank-based matching procedure.",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ),
)
@click.option(
    "--input_reference",
    "file_path_reference",
    help="Path to the reference raster opened with rasterio",
    required=True,
    type=click.Path(),
)
@click.option(
    "--input_secondary",
    "file_path_secondary",
    help="Path to the secondary image opened with skimage.io.imread",
    required=True,
    type=click.Path(),
)
@click.option(
    "--rank",
    "rank",
    help="Rank for the rank-based matching procedure",
    required=False,
    type=int,
    default=3,
)
@click.option(
    "--fdecimation",
    "fdecimation",
    help="Decimation Factor",
    required=False,
    type=int,
    default=8,
)
def mining_cli(file_path_reference, file_path_secondary, rank, fdecimation):
    """Run the mining CLI."""
    return mining(
        file_path_reference=file_path_reference,
        file_path_secondary=file_path_secondary,
        rank=rank,
        fdecimation=fdecimation,
    )


if __name__ == "__main__":
    mining_cli()
