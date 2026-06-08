import numpy as np
from scipy import signal
from scipy import ndimage

USE_LINEAR = True


def interp2(image, x_coords, y_coords):
    order = 1 if USE_LINEAR else 3
    return ndimage.map_coordinates(
        image, [y_coords, x_coords], order=order, mode="nearest"
    ).reshape(image.shape)


def conv2bis(image, weights):
    return signal.convolve2d(image, weights, mode="valid")


def conv2Sep(image, weights):
    return conv2bis(conv2bis(image, weights.T), weights)


def gradients(image):
    grad_y, grad_x = np.gradient(image)
    return grad_x, grad_y
