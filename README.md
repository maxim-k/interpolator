# Matrix Interpolator

Fill missing values in a CSV matrix by averaging non‑diagonal neighbours. Lightweight CLI built in Python, using Click and NumPy.

---

## Project layout

```
interpolator/
├── example_data/                       ← sample CSVs
│   ├── input_test_data.csv
│   └── interpolated_test_data.csv
├── matrix_interpolator/                ← package source
│   ├── cli.py          ← Click-based entry point
│   ├── core.py         ← multi-pass interpolation logic
│   ├── io.py           ← CSV read/write helpers
│   └── exceptions.py   ← custom error types
├── output/             ← place your result CSVs here
├── tests/              ← pytest suite
└── pyproject.toml      ← Poetry config & dependencies
```

---

## Installation

From the project root (where `pyproject.toml` lives):

```bash
poetry install
```

---

## Usage

```bash
python -m matrix_interpolator.cli <input_csv> <output_csv> [options]
```

* `<input_csv>`: Path to the source CSV file.
* `<output_csv>`: Path where the interpolated CSV will be written (will be created or overwritten).

### Options

* `-p, --passes N`
  Number of interpolation passes (default: 1). Each pass fills NaNs that have at least one non‑NaN neighbour. Larger clusters may require more passes.

* `-v, --verbose`
  Enable DEBUG‑level logging for detailed progress messages.

---

## Errors

* **InvalidMatrixError**
  Raised when the input CSV cannot be parsed into a proper rectangular numeric matrix (e.g., ragged rows, non-numeric values). The CLI will report this error and exit with code 1.

* **SuspiciousGapsError**
  Raised when NaNs remain after the specified number of passes. Indicates unusually large missing-value clusters. The CLI will report this error and exit with code 1.

---
## How it works

1. **Vectorized neighbour averaging**
   The core algorithm builds four shifted copies of the matrix (up, down, left, right) via `np.roll`, zeroes out the wrap‑around edges, and then computes:

   * **Sum of neighbours**: element‑wise add of the four shifted arrays (with `nan` treated as zero via `np.nan_to_num`).
   * **Count of valid neighbours**: element‑wise count of non‑NaN entries in those four shifts.
   * **Average**: divide sum by count at positions where the original cell is NaN.

2. **Performance**

   * Computation is extremely fast: all operations happen in optimized C loops inside NumPy.
   * Memory cost is higher: you temporarily allocate \~6× the original matrix size (original + 4 shifts + sum + count).
   * On a 10k×10k matrix (\~100M floats), that can be several gigabytes of RAM.

3. **Multi‑pass interpolation**

   * With `--passes N`, the tool repeats the averaging kernel N times.
   * This allows filling deeper “holes” (clusters of NaNs) in concentric rings.
   * If any NaNs remain after N passes, the tool raises an error (`SuspiciousGapsError`) to flag unusually large gaps.

Example cluster behavior:

```
1  nan  nan  4
nan nan nan nan
7  nan  nan 10
```

* **1 pass**: only edge‑adjacent NaNs get values (cells with at least one valid neighbour).
* **2 passes**: the inner NaNs (originally surrounded by NaNs) now have neighbours to average and get filled.

---

## Testing

From the project root, simply run:

```bash
pytest
```

Includes unit tests for core logic, I/O, CLI, and integration against the sample data in `example_data/`.
