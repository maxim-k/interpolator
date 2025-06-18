import numpy as np
import pandas as pd

from .exceptions import InvalidMatrixError


def read_matrix(path: str) -> np.ndarray:
    """
    Read a raw CSV file (no headers) into a 2D NumPy array of floats.
    Only numeric entries and empty cells or "nan" (any case) are allowed.
    Missing values ("" or "nan") are converted to np.nan.

    :param path: Path to the raw CSV file.
    :returns: 2D numpy.ndarray of floats.
    :raises InvalidMatrixError: If the file can’t be read or parsing fails
            (e.g. inconsistent rows or non-numeric entries).
    """
    try:
        data = np.genfromtxt(
            path,
            delimiter=",",
            dtype=float,
            missing_values=["", "nan"],
            filling_values=np.nan,
            invalid_raise=True,
        )
    except OSError as e:
        raise InvalidMatrixError(f"Error reading file '{path}': {e}")
    except ValueError as e:
        # NumPy’s ValueError will include the problematic line number
        raise InvalidMatrixError(f"Error parsing '{path}': {e}")

    # Ensure we always return a 2D array
    if data.ndim == 0:
        data = data.reshape(1, 1)
    elif data.ndim == 1:
        data = data.reshape(1, -1)

    return data


def write_matrix(arr: np.ndarray, path: str) -> None:
    """
    Write a 2D NumPy array to CSV without headers or index, using 'nan' for missing values.

    :param arr: 2D numpy.ndarray to write.
    :param path: Path for the output CSV file.
    """

    df = pd.DataFrame(arr)
    df.to_csv(path, header=False, index=False, float_format="%.6g", na_rep="nan")
