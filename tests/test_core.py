from pathlib import Path

import numpy as np
import numpy.testing as npt
import pytest

from matrix_interpolator.core import interpolate
from matrix_interpolator.exceptions import SuspiciousGapsError
from matrix_interpolator.io import read_matrix


def test_simple_fill():
    arr = np.array([[1, 2, 3], [4, np.nan, 6], [7, 8, 9]], dtype=float)
    result = interpolate(arr, passes=1)
    assert not np.isnan(result).any()
    expected = (2 + 8 + 4 + 6) / 4
    assert result[1, 1] == pytest.approx(expected)


@pytest.mark.parametrize(
    "passes,should_raise",
    [
        (0, True),  # zero passes - no fill at all
        (1, False),  # one pass fills both NaNs
    ],
)
def test_no_fill_raises(passes, should_raise):
    arr = np.array([[1, np.nan], [np.nan, 4]], dtype=float)
    if should_raise:
        with pytest.raises(SuspiciousGapsError):
            interpolate(arr, passes=passes)
    else:
        assert not np.isnan(interpolate(arr, passes=passes)).any()


def test_two_by_two_hole_mult_pass():
    arr = np.array(
        [
            [1, np.nan, np.nan, 4],
            [np.nan, np.nan, np.nan, np.nan],
            [7, np.nan, np.nan, 10],
        ],
        dtype=float,
    )
    with pytest.raises(SuspiciousGapsError):
        interpolate(arr, passes=1)
    filled = interpolate(arr, passes=2)
    assert not np.isnan(filled).any()


def test_no_nans_returns_same():
    arr = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=float)
    result = interpolate(arr, passes=1)
    assert np.array_equal(result, arr)


def test_original_not_mutated():
    arr = np.array([[np.nan, 1.0]], dtype=float)
    arr_copy = arr.copy()
    with pytest.raises(SuspiciousGapsError):
        interpolate(arr, passes=0)
    npt.assert_array_equal(arr, arr_copy)


def test_corner_and_edge_fill():
    arr = np.array(
        [
            [np.nan, 2.0, np.nan, 4.0],
            [5.0, 6.0, 7.0, 8.0],
        ],
        dtype=float,
    )
    result = interpolate(arr, passes=1)
    assert result[0, 0] == pytest.approx((2.0 + 5.0) / 2)
    assert result[0, 2] == pytest.approx((2.0 + 4.0 + 7.0) / 3)


def test_example_data():
    # Locate project root and read example_data
    root = Path(__file__).parent.parent
    in_path = root / "example_data" / "input_test_data.csv"
    out_path = root / "example_data" / "interpolated_test_data.csv"
    if not in_path.exists() or not out_path.exists():
        pytest.skip(
            "Example data not found at example_data/; skipping integration test."
        )
    input_arr = read_matrix(str(in_path))
    expected = read_matrix(str(out_path))
    result = interpolate(input_arr, passes=1)
    assert np.allclose(result, expected, atol=1e-6)
