import unittest

import numpy as np

from gefolki.tools import wrapData


class WrapDataTests(unittest.TestCase):
    def test_zero_flow_keeps_image_unchanged(self):
        image = np.arange(25, dtype=np.float32).reshape(5, 5)
        zeros = np.zeros_like(image)

        wrapped = wrapData(image, zeros, zeros)

        np.testing.assert_allclose(wrapped, image)

    def test_positive_horizontal_flow_samples_right_neighbor(self):
        image = np.arange(9, dtype=np.float32).reshape(3, 3)
        u = np.ones_like(image)
        v = np.zeros_like(image)

        wrapped = wrapData(image, u, v)

        expected = np.array(
            [
                [1.0, 2.0, 2.0],
                [4.0, 5.0, 5.0],
                [7.0, 8.0, 8.0],
            ],
            dtype=np.float32,
        )
        np.testing.assert_allclose(wrapped, expected)

    def test_positive_vertical_flow_samples_lower_neighbor(self):
        image = np.arange(9, dtype=np.float32).reshape(3, 3)
        u = np.zeros_like(image)
        v = np.ones_like(image)

        wrapped = wrapData(image, u, v)

        expected = np.array(
            [
                [3.0, 4.0, 5.0],
                [6.0, 7.0, 8.0],
                [6.0, 7.0, 8.0],
            ],
            dtype=np.float32,
        )
        np.testing.assert_allclose(wrapped, expected)


if __name__ == "__main__":
    unittest.main()
