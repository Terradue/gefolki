# First Steps with the Example Notebooks

This tutorial introduces the project through the example notebooks shipped in `examples/`.

## Recommended order

1. Start with `examples/package_usage.ipynb`
2. Continue with `examples/Mining.ipynb`

## Notebook 1: `examples/package_usage.ipynb`

Use this notebook as the quickest hands-on entry point.

What it covers:

- importing `gefolki`
- downloading the example datasets
- calling `gefolki.mining(...)` on a reference and secondary image pair
- running `gefolki.demo()` with the bundled example scenes

Why start here:

- it shows the smallest working Python surface of the library
- it exercises both the mining workflow and the built-in demo
- it is the closest thing in the repository to a quickstart notebook

## Notebook 2: `examples/Mining.ipynb`

Use this notebook after the package-usage quickstart.

What it covers:

- loading the reference and secondary images explicitly
- visualizing the input data
- downsampling for the coarse search stage
- applying the rank-based matching criterion
- refining the search in the reference crop
- visualizing the extracted match

Why it matters:

- it explains what `gefolki.mining(...)` is doing internally
- it is useful when you need to tune `rank` or `fdecimation`
- it provides a more inspectable workflow than the one-line API call

## Suggested learning path

After working through these notebooks:

- use the [Python API reference](../reference/python-api.md) to map notebook code to the supported interfaces
- use the [CLI reference](../reference/cli.md) if you want to run the mining workflow from the command line
- use the [Explanation section](../explanation/index.md) for upstream conceptual background and parameter rationale
