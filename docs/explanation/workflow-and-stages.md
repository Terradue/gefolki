# Workflow and Processing Stages

This page points to the upstream documents that explain the overall GeFolki processing chain.

## Primary source

- [manual_gefolki_english.pdf](/data/work/github-terradue/gefolki/documents/manual_gefolki_english.pdf)

## Where to read

- Manual, opening overview
  The first pages describe the three-stage decomposition of coregistration:
  1. initialization,
  2. flow calculation with GeFolki,
  3. final resampling.
- Manual, section `DESCRIPTION OF THE FIRST STEP : INITIALIZATION`
  Read this section for the role of the reference and secondary image before dense flow estimation.
- Manual, section `DESCRIPTION OF THE MAIN STEP : FLOW CALULATION BY GEFOLKI`
  Read this section for the definition of the flow matrix `W` and its components.
- Manual, section `LAST STEP : RESAMPLING`
  Read this section for the final interpolation step that applies the estimated deformation.

## Complementary visual source

- [COREGISTRATION.pdf](/data/work/github-terradue/gefolki/documents/COREGISTRATION.pdf)

Relevant slides:

- `A general scenario`
  High-level diagram of initialization, deformation computation, resampling, and validation.
- `The step of initialisation`
  Practical view of what must happen before GeFolki is used.
- `Flow estimation`
  Visual framing of feature detection and dense flow estimation.
- `Resampling`
  Summary of the final interpolation stage.
