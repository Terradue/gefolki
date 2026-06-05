import unittest
from contextlib import ExitStack
from unittest.mock import patch

import numpy as np
from click.testing import CliRunner

from gefolki.mining import mining


class _FakeRaster:
    def __init__(self, array):
        self._array = array

    def read(self):
        return self._array


class MiningCliTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def _patched_runtime(self, master=None, slave=None, open_side_effect=None):
        if master is None:
            master = np.arange(64 * 64, dtype=np.float32).reshape(1, 64, 64)
        if slave is None:
            slave_band = np.arange(64, dtype=np.float32).reshape(8, 8)
            slave = np.dstack((slave_band, slave_band, slave_band))

        def _fake_resize(arr, shape, *args):
            return arr[: shape[0], : shape[1]]

        stack = ExitStack()
        if open_side_effect is None:
            stack.enter_context(
                patch("gefolki.mining.rasterio.open", return_value=_FakeRaster(master))
            )
        else:
            stack.enter_context(
                patch("gefolki.mining.rasterio.open", side_effect=open_side_effect)
            )
        stack.enter_context(patch("gefolki.mining.imread", return_value=slave))
        stack.enter_context(
            patch("gefolki.mining.rank_filter_inf", side_effect=lambda arr, _: arr)
        )
        stack.enter_context(patch("gefolki.mining.resize", side_effect=_fake_resize))
        stack.enter_context(patch("gefolki.mining.pl.figure"))
        stack.enter_context(patch("gefolki.mining.pl.imshow"))
        stack.enter_context(patch("gefolki.mining.pl.title"))
        stack.enter_context(patch("gefolki.mining.pl.show"))
        stack.enter_context(patch("gefolki.mining.logger.info"))
        stack.enter_context(patch("gefolki.mining.logger.success"))
        return stack

    def test_requires_input_paths(self):
        result = self.runner.invoke(mining, [])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing option", result.output)
        self.assertIn("--input_master", result.output)

    def test_requires_slave_when_master_is_provided(self):
        result = self.runner.invoke(mining, ["--input_master", "master.tif"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing option", result.output)
        self.assertIn("--input_slave", result.output)

    def test_help_lists_expected_options(self):
        result = self.runner.invoke(mining, ["--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("--input_master", result.output)
        self.assertIn("--input_slave", result.output)
        self.assertIn("--rank", result.output)
        self.assertIn("--fdecimation", result.output)

    def test_rejects_non_integer_rank(self):
        result = self.runner.invoke(
            mining,
            [
                "--input_master",
                "master.tif",
                "--input_slave",
                "slave.png",
                "--rank",
                "bad",
            ],
        )

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Invalid value", result.output)
        self.assertIn("--rank", result.output)

    def test_rejects_non_integer_fdecimation(self):
        result = self.runner.invoke(
            mining,
            [
                "--input_master",
                "master.tif",
                "--input_slave",
                "slave.png",
                "--fdecimation",
                "bad",
            ],
        )

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Invalid value", result.output)
        self.assertIn("--fdecimation", result.output)

    def test_runs_with_required_inputs(self):
        with self._patched_runtime():
            result = self.runner.invoke(
                mining,
                [
                    "--input_master",
                    "master.tif",
                    "--input_slave",
                    "slave.png",
                    "--rank",
                    "3",
                    "--fdecimation",
                    "1",
                ],
            )

        self.assertEqual(result.exit_code, 0, result.output)

    def test_runs_with_default_optional_arguments(self):
        with self._patched_runtime():
            result = self.runner.invoke(
                mining,
                [
                    "--input_master",
                    "master.tif",
                    "--input_slave",
                    "slave.png",
                ],
            )

        self.assertEqual(result.exit_code, 0, result.output)

    def test_callback_returns_expected_extraction_tuple(self):
        with self._patched_runtime():
            result = mining.callback(
                file_path_master="master.tif",
                file_path_slave="slave.png",
                rank=3,
                fdecimation=1,
            )

        # The current implementation derives ymax from xmax instead of ymin.
        self.assertEqual(result[:4], (0, 8, 0, 16))
        self.assertEqual(result[4].shape, (8, 8))

    def test_fails_when_master_open_fails(self):
        with self._patched_runtime(open_side_effect=FileNotFoundError("missing master")):
            result = self.runner.invoke(
                mining,
                [
                    "--input_master",
                    "missing.tif",
                    "--input_slave",
                    "slave.png",
                ],
            )

        self.assertNotEqual(result.exit_code, 0)
        self.assertIsInstance(result.exception, FileNotFoundError)

    def test_fails_when_slave_read_fails(self):
        with self._patched_runtime() as stack:
            stack.enter_context(
                patch("gefolki.mining.imread", side_effect=FileNotFoundError("missing slave"))
            )
            result = self.runner.invoke(
                mining,
                [
                    "--input_master",
                    "master.tif",
                    "--input_slave",
                    "missing.png",
                ],
            )

        self.assertNotEqual(result.exit_code, 0)
        self.assertIsInstance(result.exception, FileNotFoundError)


if __name__ == "__main__":
    unittest.main()
