# Run the Mining Workflow from Python

This guide is based on `examples/package_usage.ipynb` and `examples/Mining.ipynb`.

## Goal

Find a smaller secondary image inside a larger reference raster from Python.

## Inputs

You need:

- a reference raster path
- a secondary image path
- optionally, `rank`
- optionally, `fdecimation`

## Minimal call

```python
import gefolki

xmin, xmax, ymin, ymax, reference_final = gefolki.mining(
    "datasets/S1_Jacksonville_GEE.tif",
    "datasets/JacksonvilleNavalAirStation_sandiaKu.png",
)
```

## Tuned call

```python
import gefolki

xmin, xmax, ymin, ymax, reference_final = gefolki.mining(
    file_path_reference="datasets/S1_Jacksonville_GEE.tif",
    file_path_secondary="datasets/JacksonvilleNavalAirStation_sandiaKu.png",
    rank=4,
    fdecimation=8,
)
```

## What happens

The mining workflow:

1. loads the reference raster and secondary image
2. computes a coarse search on downsampled data
3. refines the match in a cropped reference region
4. returns the bounding coordinates and extracted reference patch
5. displays diagnostic Matplotlib figures

## When to open the notebook

If you want to inspect the intermediate steps, open:

- `examples/Mining.ipynb`

That notebook breaks the algorithm into the same stages used by `gefolki.mining(...)`.
