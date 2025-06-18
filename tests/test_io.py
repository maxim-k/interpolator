import numpy as np
import pytest

from matrix_interpolator.exceptions import InvalidMatrixError
from matrix_interpolator.io import read_matrix, write_matrix


def test_read_write_roundtrip(tmp_path):
    arr = np.array([[1.1, np.nan], [3.3, 4.4]], dtype=float)
    input_path = tmp_path / "in.csv"
    write_matrix(arr, str(input_path))
    read = read_matrix(str(input_path))
    assert np.allclose(np.nan_to_num(read), np.nan_to_num(arr))
    assert np.isnan(read[0, 1]) and np.isnan(arr[0, 1])


def test_invalid_matrix(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text(
        """1,2,3
4,5
"""
    )
    with pytest.raises(InvalidMatrixError):
        read_matrix(str(bad))
