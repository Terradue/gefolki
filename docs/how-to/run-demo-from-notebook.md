# Run the Built-in Demo from a Notebook

This guide is based on `examples/package_usage.ipynb`.

## Goal

Run the built-in GeFolki demo with the example datasets.

## Required files

The demo expects these local files:

- `datasets/radar_bandep.png`
- `datasets/lidar_georef.png`
- `datasets/optiquehr_georef.png`

## Minimal notebook flow

```python
import gefolki
```

Download the datasets, then run:

```python
gefolki.demo()
```

## What the demo shows

The demo runs two visual workflows:

- LiDAR/radar registration
- optical/radar registration

It displays:

- input images
- displacement norm views
- before/after fused visualizations

## Notebook source

For the original runnable example, see:

- `examples/package_usage.ipynb`
