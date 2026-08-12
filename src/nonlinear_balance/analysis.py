"""
Analysis and validation tools for nonlinear balance solutions.
"""

import numpy as np


def conservation_error(result, initial_total=1.0):
    """
    Compute the relative conservation error.

    The model should satisfy

        P + A + B = constant.
    """

    total = (
        result["P"]
        + result["A"]
        + result["B"]
    )

    error = np.abs(
        total - initial_total
    ) / initial_total

    return error


def analytical_control_solution(t, P0, A0, B0, k_A):
    """
    Analytical solution for the control model k_B = 0.
    """

    A = A0 * np.exp(-k_A * t)

    B = np.full_like(
        t,
        B0,
        dtype=float,
    )

    P = P0 + A0 * (
        1.0 - np.exp(-k_A * t)
    )

    return {
        "P": P,
        "A": A,
        "B": B,
    }


def activation_time(result, K):
    """
    Return the first time at which P >= K.
    """

    idx = np.where(
        result["P"] >= K
    )[0]

    if len(idx) == 0:
        return np.nan

    return result["t"][idx[0]]


def crossover_time(result):
    """
    Return the first time at which R_B >= R_A.
    """

    idx = np.where(
        result["R_B"] >= result["R_A"]
    )[0]

    if len(idx) == 0:
        return np.nan

    return result["t"][idx[0]]


def control_errors(numerical, analytical):
    """
    Maximum absolute errors with respect to
    the analytical control solution.
    """

    return {
        "P": np.max(
            np.abs(
                numerical["P"]
                - analytical["P"]
            )
        ),
        "A": np.max(
            np.abs(
                numerical["A"]
                - analytical["A"]
            )
        ),
        "B": np.max(
            np.abs(
                numerical["B"]
                - analytical["B"]
            )
        ),
    }



def conversion_time(
    result,
    P0,
    A0,
    B0,
    fraction,
):
    """
    Return the first time at which a given fraction
    of the initial reservoirs has been converted.
    """

    target = P0 + fraction * (A0 + B0)

    idx = np.where(
        result["P"] >= target
    )[0]

    if len(idx) == 0:
        return np.nan

    return result["t"][idx[0]]



def state_at_time(
    result,
    time,
):
    """
    Return the system state at the grid point closest
    to a specified time.
    """

    if not np.isfinite(time):
        return {
            "P": np.nan,
            "A": np.nan,
            "B": np.nan,
            "R_A": np.nan,
            "R_B": np.nan,
        }

    idx = np.argmin(
        np.abs(result["t"] - time)
    )

    return {
        "P": result["P"][idx],
        "A": result["A"][idx],
        "B": result["B"][idx],
        "R_A": result["R_A"][idx],
        "R_B": result["R_B"][idx],
    }