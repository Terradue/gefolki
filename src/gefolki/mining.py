"""
Date : 01/10/2018
"""

from __future__ import absolute_import
import numpy as np

# from algorithm import EFolki
from skimage.io import imread
from skimage.transform import resize

# from rank import rank_sup as rank_filter_sup
from .rank import rank_inf as rank_filter_inf
import rasterio
from loguru import logger


def _get_plot_module():
    import matplotlib.pyplot as pl

    return pl


def mining(
    file_path_reference=None,
    file_path_secondary=None,
    rank=3,
    fdecimation=8,
    **deprecated_kwargs,
):
    """Load a raster."""
    if "file_path_master" in deprecated_kwargs and file_path_reference is None:
        file_path_reference = deprecated_kwargs.pop("file_path_master")
    if "file_path_slave" in deprecated_kwargs and file_path_secondary is None:
        file_path_secondary = deprecated_kwargs.pop("file_path_slave")
    if deprecated_kwargs:
        unexpected = ", ".join(sorted(deprecated_kwargs))
        raise TypeError(f"Unexpected keyword arguments: {unexpected}")

    pl = _get_plot_module()
    logger.info("Mining Execution Started")
    src = rasterio.open(file_path_reference)
    raster_data = src.read()
    reference_image = raster_data[0, :, :]

    pl.figure()
    pl.imshow(reference_image)
    pl.title("Reference")

    secondary_data = imread(file_path_secondary)
    pl.figure()
    pl.imshow(secondary_data)
    pl.title("Secondary: Image to find within the Reference")

    secondary_image = secondary_data[:, :, 0]
    dimx, dimy = np.shape(reference_image)
    dimxn, dimyn = np.shape(secondary_image)

    # Decimation

    nx = int(round(dimx / fdecimation))
    ny = int(round(dimy / fdecimation))
    reference_downsampled = resize(reference_image, (nx, ny), 1, "constant")
    nsx = int(round(dimxn / fdecimation))
    nsy = int(round(dimyn / fdecimation))
    secondary_downsampled = resize(secondary_image, (nsx, nsy), 1, "constant")

    # Rank computation and Criterion on images after deximation
    reference_rank = rank_filter_inf(
        reference_downsampled, rank
    )  # rank sup : high value pixels have low rank
    secondary_rank = rank_filter_inf(secondary_downsampled, rank)

    R = np.zeros((nx - nsx - 1, ny - nsy - 1))
    indices = np.nonzero(secondary_rank)
    test2 = secondary_rank[indices]

    for k in range(0, nx - nsx - 1):
        for p in range(0, ny - nsy - 1):
            test1 = reference_rank[k : k + nsx, p : p + nsy]
            test1 = test1[indices]
            test = (test1 - test2) ** 2
            R[k, p] = test.mean()

    pl.figure()
    pl.imshow(R, vmin=np.min(R[np.nonzero(R)]), vmax=R.max(), cmap="jet")
    pl.title("Criterion after decimation")

    ind = np.unravel_index(np.argmin(R, axis=None), R.shape)
    indx = ind[0] * fdecimation
    indy = ind[1] * fdecimation

    indx1 = max(0, indx - 100)
    indx1max = min(dimx, indx + dimxn + 100)
    indy1 = max(0, indy - 100)
    indy1max = min(dimy, indy + dimyn + 100)

    # Rank computation and Criterion on images without deximation after preinitialization
    reference_crop = reference_image[indx1:indx1max, indy1:indy1max]
    reference_rank_crop = rank_filter_inf(
        reference_crop, rank
    )  # rank sup : high value pixels have low rank
    secondary_rank_full = rank_filter_inf(secondary_image, rank)

    dimxcrop, dimycrop = np.shape(reference_rank_crop)
    Rfin = np.zeros((dimxcrop - dimxn - 1, dimycrop - dimyn - 1))
    indices = np.nonzero(secondary_rank_full)
    test2 = secondary_rank_full[indices]

    for k in range(0, dimxcrop - dimxn - 1):
        for p in range(0, dimycrop - dimyn - 1):
            test1 = reference_rank_crop[k : k + dimxn, p : p + dimyn]
            test1 = test1[indices]
            test = (test1 - test2) ** 2
            Rfin[k, p] = test.mean()

    # Final Extraction
    ind = np.unravel_index(np.argmin(Rfin, axis=None), Rfin.shape)
    indx2 = ind[0]
    indy2 = ind[1]
    reference_final = reference_crop[indx2 : indx2 + dimxn, indy2 : indy2 + dimyn]

    pl.figure()
    pl.imshow(Rfin, vmin=np.min(Rfin[np.nonzero(Rfin)]), vmax=Rfin.max(), cmap="jet")
    pl.title("Fine Criterion without decimation after preinitialisation")

    rgb = np.dstack((secondary_image, reference_final, secondary_image))

    pl.figure()
    pl.imshow(rgb)
    pl.title("Superposition of Secondary and Reference Extraction")

    pl.show()

    xmin = indx1 + indx2
    ymin = indy1 + indy2
    xmax = xmin + dimxn
    ymax = xmax + dimyn
    logger.info(
        f"Final extraction coordinates: xmin={xmin}, xmax={xmax}, ymin={ymin}, ymax={ymax}"
    )
    logger.success("Done")
    return xmin, xmax, ymin, ymax, reference_final


# EOF
