import importlib
import unittest
from contextlib import ExitStack
from unittest.mock import patch
from types import SimpleNamespace

import numpy as np
from click.testing import CliRunner

from gefolki.cli import mining_cli
from gefolki.mining import mining

mining_module = importlib.import_module("gefolki.mining")


class _FakeRaster:
    def __init__(self, array):
        self._array = array

    def read(self):
        return self._array


class MiningCliTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def _patched_runtime(self, reference=None, secondary=None, open_side_effect=None):
        if reference is None:
            reference = np.arange(64 * 64, dtype=np.float32).reshape(1, 64, 64)
        if secondary is None:
            secondary_band = np.arange(64, dtype=np.float32).reshape(8, 8)
            secondary = np.dstack((secondary_band, secondary_band, secondary_band))

        def _fake_resize(arr, shape, *args):
            return arr[: shape[0], : shape[1]]

        plot_stub = SimpleNamespace(
            figure=lambda *args, **kwargs: None,
            imshow=lambda *args, **kwargs: None,
            title=lambda *args, **kwargs: None,
            show=lambda *args, **kwargs: None,
        )

        stack = ExitStack()
        if open_side_effect is None:
            stack.enter_context(
                patch.object(
                    mining_module.rasterio, "open", return_value=_FakeRaster(reference)
                )
            )
        else:
            stack.enter_context(
                patch.object(mining_module.rasterio, "open", side_effect=open_side_effect)
            )
        stack.enter_context(patch.object(mining_module, "imread", return_value=secondary))
        stack.enter_context(
            patch.object(mining_module, "rank_filter_inf", side_effect=lambda arr, _: arr)
        )
        stack.enter_context(patch.object(mining_module, "resize", side_effect=_fake_resize))
        stack.enter_context(
            patch.object(mining_module, "_get_plot_module", return_value=plot_stub)
        )
        stack.enter_context(patch.object(mining_module.logger, "info"))
        stack.enter_context(patch.object(mining_module.logger, "success"))
        return stack

    def test_requires_input_paths(self):
        result = self.runner.invoke(mining_cli, [])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing option", result.output)
        self.assertIn("--input_reference", result.output)

    def test_requires_secondary_when_reference_is_provided(self):
        result = self.runner.invoke(mining_cli, ["--input_reference", "reference.tif"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing option", result.output)
        self.assertIn("--input_secondary", result.output)

    def test_help_lists_expected_options(self):
        result = self.runner.invoke(mining_cli, ["--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("--input_reference", result.output)
        self.assertIn("--input_secondary", result.output)
        self.assertIn("--rank", result.output)
        self.assertIn("--fdecimation", result.output)

    def test_rejects_non_integer_rank(self):
        result = self.runner.invoke(
            mining_cli,
            [
                "--input_reference",
                "reference.tif",
                "--input_secondary",
                "secondary.png",
                "--rank",
                "bad",
            ],
        )

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Invalid value", result.output)
        self.assertIn("--rank", result.output)

    def test_rejects_non_integer_fdecimation(self):
        result = self.runner.invoke(
            mining_cli,
            [
                "--input_reference",
                "reference.tif",
                "--input_secondary",
                "secondary.png",
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
                mining_cli,
                [
                    "--input_reference",
                    "reference.tif",
                    "--input_secondary",
                    "secondary.png",
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
                mining_cli,
                [
                    "--input_reference",
                    "reference.tif",
                    "--input_secondary",
                    "secondary.png",
                ],
            )

        self.assertEqual(result.exit_code, 0, result.output)

    def test_direct_function_returns_expected_extraction_tuple(self):
        with self._patched_runtime():
            result = mining(
                file_path_reference="reference.tif",
                file_path_secondary="secondary.png",
                rank=3,
                fdecimation=1,
            )

        # The current implementation derives ymax from xmax instead of ymin.
        self.assertEqual(result[:4], (0, 8, 0, 16))
        self.assertEqual(result[4].shape, (8, 8))

    def test_fails_when_reference_open_fails(self):
        with self._patched_runtime(
            open_side_effect=FileNotFoundError("missing reference")
        ):
            result = self.runner.invoke(
                mining_cli,
                [
                    "--input_reference",
                    "missing.tif",
                    "--input_secondary",
                    "secondary.png",
                ],
            )

        self.assertNotEqual(result.exit_code, 0)
        self.assertIsInstance(result.exception, FileNotFoundError)

    def test_fails_when_secondary_read_fails(self):
        with self._patched_runtime() as stack:
            stack.enter_context(
                patch.object(
                    mining_module,
                    "imread",
                    side_effect=FileNotFoundError("missing secondary"),
                )
            )
            result = self.runner.invoke(
                mining_cli,
                [
                    "--input_reference",
                    "reference.tif",
                    "--input_secondary",
                    "missing.png",
                ],
            )

        self.assertNotEqual(result.exit_code, 0)
        self.assertIsInstance(result.exception, FileNotFoundError)


if __name__ == "__main__":
    unittest.main()
