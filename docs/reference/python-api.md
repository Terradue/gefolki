# Python API

This page documents the public Python interfaces exported by `gefolki`.

## Package Exports

The top-level package currently re-exports:

- `gefolki.Folki`
- `gefolki.EFolki`
- `gefolki.GEFolki`
- `gefolki.wrapData`
- `gefolki.mining`
- `gefolki.rank_filter_inf`
- `gefolki.rank_filter_sup`
- `gefolki.demo`

## Dense Registration Interfaces

### `gefolki.Folki`

Dense registration callable for homogeneous image pairs.

Signature:

```python
u, v = gefolki.Folki(I0, I1, *, levels=4, iteration=5, radius=8, talon=1.0e-8, uinit=None, vinit=None)
```

Parameters:

- `I0`
  Reference image as a 2D NumPy array.
- `I1`
  Secondary image as a 2D NumPy array, already initialized to the reference geometry.
- `levels`
  Number of pyramid levels used by the multiscale wrapper.
- `iteration`
  Number of iterations at each scale.
- `radius`
  Window radius for local averaging.
- `talon`
  Small stabilization term added to structure-tensor terms.
- `uinit`, `vinit`
  Optional initial displacement fields.

Returns:

- `u`
  Horizontal displacement field with the same shape as `I0`.
- `v`
  Vertical displacement field with the same shape as `I0`.

### `gefolki.EFolki`

Dense registration callable with rank-based preprocessing for more difficult remote-sensing texture.

Signature:

```python
u, v = gefolki.EFolki(I0, I1, *, levels=4, iteration=5, radius=[8, 4], rank=4, uinit=None, vinit=None)
```

Additional parameters:

- `radius`
  Sequence of window radii evaluated from coarse to fine inside each pyramid level.
- `rank`
  Rank-filter radius used before optical-flow estimation.

Returns:

- `u`
  Horizontal displacement field.
- `v`
  Vertical displacement field.

### `gefolki.GEFolki`

Dense registration callable for heterogeneous image pairs, with rank filtering and contrast adaptation.

Signature:

```python
u, v = gefolki.GEFolki(I0, I1, *, levels=4, iteration=5, radius=[8, 4], rank=4, uinit=None, vinit=None)
```

Notes:

- Intended for heterogeneous modalities such as SAR/optical or SAR/LiDAR.
- Internally applies rank filtering and adaptive histogram equalization before displacement estimation.

Returns:

- `u`
  Horizontal displacement field.
- `v`
  Vertical displacement field.

## Warping Helper

### `gefolki.wrapData(image, u, v)`

Applies a dense displacement field to an image using nearest-edge handling.

Parameters:

- `image`
  Input 2D array to warp.
- `u`
  Horizontal displacement field.
- `v`
  Vertical displacement field.

Returns:

- Warped image as a NumPy array with the same shape as `image`.

## Rank Filters

### `gefolki.rank_filter_inf(image, rad)`

Computes a local rank image by counting neighbors with lower intensity than each pixel.

Parameters:

- `image`
  Input 2D array.
- `rad`
  Neighborhood radius.

Returns:

- Rank image as a NumPy array.

### `gefolki.rank_filter_sup(image, rad)`

Computes a local rank image by counting neighbors with higher intensity than each pixel.

Parameters:

- `image`
  Input 2D array.
- `rad`
  Neighborhood radius.

Returns:

- Rank image as a NumPy array.

## Mining Workflow

### `gefolki.mining(file_path_reference=None, file_path_secondary=None, rank=3, fdecimation=8, **deprecated_kwargs)`

Searches for a smaller secondary image inside a larger reference raster using a coarse-to-fine rank-based criterion.

Parameters:

- `file_path_reference`
  Path to the reference raster opened with `rasterio`.
- `file_path_secondary`
  Path to the secondary image opened with `skimage.io.imread`.
- `rank`
  Rank-filter radius.
- `fdecimation`
  Decimation factor used in the coarse search.

Backward compatibility:

- The function still accepts legacy keyword arguments `file_path_master` and `file_path_slave`.

Returns:

```python
xmin, xmax, ymin, ymax, reference_final
```

Where:

- `xmin`, `xmax`
  Horizontal bounds of the best match in reference-image coordinates.
- `ymin`, `ymax`
  Vertical bounds of the best match in reference-image coordinates.
- `reference_final`
  Extracted reference subimage matching the secondary-image footprint.

Side effects:

- Opens interactive plotting windows through Matplotlib.
- Logs progress through `loguru`.

## Demo

### `gefolki.demo()`

Runs the built-in visual demonstration workflows for LiDAR/radar and optical/radar registration.

Expected local files:

- `./datasets/radar_bandep.png`
- `./datasets/lidar_georef.png`
- `./datasets/optiquehr_georef.png`

Side effects:

- Displays Matplotlib figures.
- Logs progress through `loguru`.
