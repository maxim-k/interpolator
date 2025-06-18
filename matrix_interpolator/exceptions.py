class SuspiciousGapsError(Exception):
    """
    Raised when NaN gaps remain after all interpolation passes.
    """

    pass


class InvalidMatrixError(Exception):
    """
    If the file can’t be read or parsing fails (e.g. inconsistent rows or non-numeric entries).
    """

    pass
