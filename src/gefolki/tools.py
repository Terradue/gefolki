from __future__ import absolute_import
import numpy as np
from .primitive import interp2


def wrapData(image, u, v):
    """
    Apply the [u,v] optical flow to the input image.
    """
    col, row = image.shape[1], image.shape[0]
    x_coords, y_coords = np.meshgrid(range(col), range(row))
    result = interp2(image, x_coords + u, y_coords + v)
    return result
