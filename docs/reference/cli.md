# CLI Interface

This page documents the public command-line interface provided by the package.

## Entry Point

After installation, the package exposes:

```bash
gefolki-mining
```

This command is implemented by `gefolki.cli:mining_cli`.

## Synopsis

```bash
gefolki-mining \
  --input_reference REFERENCE.tif \
  --input_secondary SECONDARY.png \
  [--rank 3] \
  [--fdecimation 8]
```

## Purpose

`gefolki-mining` searches for a smaller secondary image inside a larger reference image using a coarse-to-fine rank-based matching procedure.

## Options

### `--input_reference`

Required.

Path to the reference raster. The implementation opens this file with `rasterio` and currently uses the first raster band as the search image.

### `--input_secondary`

Required.

Path to the secondary image. The implementation opens this file with `skimage.io.imread` and currently uses the first channel as the search image.

### `--rank`

Optional. Default: `3`

Rank-filter radius used in both the coarse and fine matching steps.

### `--fdecimation`

Optional. Default: `8`

Decimation factor used in the coarse search stage.

## Behavior

When executed, the command:

1. Loads the reference raster and secondary image.
2. Builds a decimated coarse search grid.
3. Computes rank-based matching scores.
4. Refines the search within a cropped region of the reference image.
5. Displays diagnostic plots with Matplotlib.
6. Logs the extracted coordinate bounds.

## Return Value

The CLI delegates to `gefolki.mining(...)`, which returns:

```python
xmin, xmax, ymin, ymax, reference_final
```

On the command line, the main user-visible outputs are the generated plots and the logged coordinates.

## Example

```bash
gefolki-mining \
  --input_reference datasets/S1_Jacksonville_GEE.tif \
  --input_secondary datasets/JacksonvilleNavalAirStation_sandiaKu.png \
  --rank 3 \
  --fdecimation 8
```

## Notes

- The CLI uses `reference` and `secondary` terminology in its public options.
- The older `master` and `slave` names are not exposed in the CLI.
- The implementation expects image data that can be indexed as 2D arrays after selecting band or channel 0.
