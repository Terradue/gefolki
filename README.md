# gefolki

GeFolki is a dense image coregistration library for remote sensing. It is designed for SAR/SAR registration and also for heterogeneous pairs such as SAR/optical, SAR/LiDAR, or hyperspectral/optical when a coarse initialization is already available.

The package estimates a dense displacement field between a master image and a slave image, then lets you resample the slave image onto the master geometry. The method is based on optical-flow-style matching adapted to remote sensing imagery, including rank filtering, multiscale pyramids, and a contrast inversion strategy for heterogeneous data.

## What GeFolki Does

GeFolki is the middle step of a three-step coregistration workflow described in the project documentation:

1. Initialization
   Put the slave image into roughly the same geometry, extent, and pixel grid as the master image.
2. Dense flow estimation
   Estimate the per-pixel displacement field between the two aligned images.
3. Resampling
   Warp the slave image with the estimated displacement field.

GeFolki handles steps 2 and 3 directly. Step 1 is intentionally external because it depends on sensor geometry, control points, geocoding, DEMs, orbit data, or a simpler crop/resize/rotation workflow.

## When To Use Which Method

The library exposes three dense registration variants:

- `Folki`
  Best suited to more standard optical-flow conditions where brightness consistency is reasonable.
- `EFolki`
  Adds rank-based filtering to improve robustness for remote sensing imagery and texture changes.
- `GEFolki`
  Adds contrast adaptation and is intended for heterogeneous image pairs such as radar/optical or radar/LiDAR.

In practice:

- Use `Folki` for homogeneous image pairs with relatively consistent appearance.
- Use `EFolki` for homogeneous remote sensing pairs that need more robustness.
- Use `GEFolki` for heterogeneous modalities or local contrast inversion cases.

## Key Capabilities

- Dense sub-image matching on a full grid
- Multiscale pyramid search for larger displacements
- Rank-filter-based matching for difficult remote sensing textures
- Contrast inversion handling for heterogeneous imagery
- Resampling of the slave image from the estimated flow
- A CLI utility to search a smaller slave image inside a larger master raster

## Installation

### From source with pip

```bash
python -m pip install .
```

### From PyPI

```bash
pip install gefolki
```

## Input and Output Model

### Inputs to dense registration

All three main registration functions expect:

- `I0`: master image as a 2D array
- `I1`: slave image as a 2D array, already initialized to the master grid
- algorithm parameters such as `radius`, `levels`, `iteration`, and `rank`

The arrays are normalized internally by the pyramid wrapper, but input images should still be numerically well-behaved and represent meaningful intensity structure.

### Outputs from dense registration

The registration functions return two arrays:

- `u`: horizontal displacement field
- `v`: vertical displacement field

Both arrays have the same shape as the input images. Together they define the dense deformation needed to warp the slave image onto the master image.



## CLI: Mining Workflow

The package exposes one command-line entry point:

```bash
gefolki-mining --input_master MASTER.tif --input_slave SLAVE.png --rank 3 --fdecimation 8
```

This workflow searches for a smaller slave image inside a larger master image using a coarse-to-fine rank-based matching procedure.

### Mining inputs

- `--input_master`
  Path to the master raster opened with `rasterio`
- `--input_slave`
  Path to the slave image opened with `skimage.io.imread`
- `--rank`
  Rank filter radius
- `--fdecimation`
  Decimation factor for the coarse search

### Mining outputs

The function `gefolki.mining.mining(...)` returns:

- `xmin`
- `xmax`
- `ymin`
- `ymax`
- `Master_final`

These correspond to the detected bounding box in the master image and the extracted matching subimage. The CLI currently visualizes the process and prints basic execution messages rather than writing a structured file output.

## Demo Workflow

The built-in demo expects these local files:

- `./datasets/radar_bandep.png`
- `./datasets/lidar_georef.png`
- `./datasets/optiquehr_georef.png`

Example:

```python
import gefolki

gefolki.demo()
```

The demo:

- computes a LiDAR/radar registration example
- computes an optical/radar registration example
- displays the displacement norm
- displays before/after fused visualizations

## References

The original manuals cite these publications for scientific use:

- Aurélien Plyer, Elise Colin-Koeniguer, Flora Weissgerber, "A New Coregistration Algorithm for Recent Applications on Urban SAR Images", IEEE Geoscience and Remote Sensing Letters, 2015.
- Guillaume Brigot, Elise Colin-Koeniguer, Aurélien Plyer, Fabrice Janez, "Adaptation and Evaluation of an Optical Flow Method Applied to Coregistration of Forest Remote Sensing Images", IEEE JSTARS, 2016.

If you use GeFolki in scientific work, cite the publication that matches your homogeneous or heterogeneous registration scenario.

## License

This repository currently contains an MIT `LICENSE.txt`, while the original project manuals and legacy packaging metadata describe the software as distributed under a GPL license. That discrepancy should be resolved before publishing or redistributing packaged releases.
