import numpy as np

from .exceptions import SuspiciousGapsError


def interpolate(arr: np.ndarray, passes: int = 1) -> np.ndarray:
    """
    Fill NaN entries in `arr` by averaging non-diagonal neighbours over multiple passes.

    :param arr: 2D numpy array with NaNs marking missing values.
    :param passes: Number of iterative passes to perform (default is 1).
    :returns: A new array with NaNs filled or raises if gaps remain.
    :raises SuspiciousGapsError: If after `passes` iterations NaNs still exist.
    """
    # Copy once to avoid mutating user data
    result = arr.copy()

    for _ in range(passes):
        # Shifted views for neighbours; wrap-around cleared after roll
        up = np.roll(result, -1, axis=0)
        down = np.roll(result, 1, axis=0)
        left = np.roll(result, -1, axis=1)
        right = np.roll(result, 1, axis=1)

        # Mask wrap-around artifacts
        up[-1, :] = np.nan
        down[0, :] = np.nan
        left[:, -1] = np.nan
        right[:, 0] = np.nan

        # Sum and count of valid neighbours
        neighbours_sum = (
            np.nan_to_num(up)
            + np.nan_to_num(down)
            + np.nan_to_num(left)
            + np.nan_to_num(right)
        )
        neighbours_count = (
            (~np.isnan(up)).astype(int)
            + (~np.isnan(down)).astype(int)
            + (~np.isnan(left)).astype(int)
            + (~np.isnan(right)).astype(int)
        )

        # Identify positions to fill: currently NaN and having >0 valid neighbours
        mask = np.isnan(result)
        valid = neighbours_count > 0
        fill_positions = mask & valid

        # Fill new values
        result[fill_positions] = (
            neighbours_sum[fill_positions] / neighbours_count[fill_positions]
        )

    # After all passes, ensure no NaNs remain
    remaining = np.isnan(result).sum()
    if remaining > 0:
        raise SuspiciousGapsError(
            f"{remaining} cells left unfilled after {passes} passes"
        )

    return result
