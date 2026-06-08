# Parameter Selection

This page points to the upstream guidance for choosing GeFolki parameters.

## Primary source

- [manual_gefolki_english.pdf](/data/work/github-terradue/gefolki/documents/manual_gefolki_english.pdf)

## Where to read

- Manual, section `DESCRIPTION OF THE MAIN STEP : FLOW CALULATION BY GEFOLKI`
  This is the main parameter reference for the algorithm.
- Manual, example parameter structure
  The `para = struct(...)` block shows the original recommended parameter layout used by the upstream MATLAB implementation.

## Parameter topics covered there

Use the manual’s numbered list in that section for:

- `radius`
  Window-size tradeoff between robustness and local detail.
- `levels`
  Pyramid depth as a function of the maximum displacement to estimate.
- `iter`
  Number of gradient-based minimization iterations.
- `contrast_adapt`
  When contrast inversion handling should be enabled for heterogeneous imagery.
- `rank`
  Rank-filter window guidance and typical values.

## Why this page is intentionally brief

The upstream manual already gives the authoritative conceptual guidance for these parameters. This local documentation keeps the explanation layer lightweight and points readers back to the original source instead of restating it inconsistently.
