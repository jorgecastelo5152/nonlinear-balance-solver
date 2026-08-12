"""
Parameter-sweep utilities for nonlinear balance systems.
"""

import itertools

import numpy as np

from .solver import solve_balance_system
from .analysis import (
    activation_time,
    crossover_time,
    conservation_error,
    conversion_time,
    state_at_time,
)


def iter_parameter_grid(grid):
    """
    Generate all combinations of a Cartesian parameter grid.

    Parameters
    ----------
    grid : dict
        Dictionary containing the parameter values to explore.

    Yields
    ------
    dict
        One parameter combination at a time.

    Example
    -------
    grid = {
        "k_B": [0.1, 1.0],
        "K": [0.1, 0.2],
        "n": [1, 2],
    }
    """

    keys = list(grid.keys())
    values = [grid[key] for key in keys]

    for combination in itertools.product(*values):
        yield dict(zip(keys, combination))


def summarize_run(result, params):
    """
    Extract summary diagnostics from a single simulation.

    The summary includes characteristic times, reservoir depletion,
    integrated channel contributions, states at selected conversion
    times, final values, and numerical conservation diagnostics.
    """

    # ========================================================
    # Conservation
    # ========================================================

    initial_total = (
        params["P0"]
        + params["A0"]
        + params["B0"]
    )

    cons_error = conservation_error(
        result,
        initial_total=initial_total,
    )

    # ========================================================
    # Instantaneous secondary-channel contribution
    # ========================================================

    total_rate = (
        result["R_A"]
        + result["R_B"]
    )

    secondary_fraction = np.divide(
        result["R_B"],
        total_rate,
        out=np.zeros_like(total_rate),
        where=total_rate > 0.0,
    )

    # ========================================================
    # Final state
    # ========================================================

    final_P = result["P"][-1]
    final_A = result["A"][-1]

    # Tiny negative values may appear when B is effectively
    # depleted because of floating-point roundoff.
    final_B = max(
        result["B"][-1],
        0.0,
    )

    # ========================================================
    # Integrated conversion
    # ========================================================

    converted_A = (
        params["A0"]
        - final_A
    )

    converted_B = (
        params["B0"]
        - final_B
    )

    total_converted = (
        converted_A
        + converted_B
    )

    if total_converted > 0.0:
        integrated_secondary_fraction = (
            converted_B
            / total_converted
        )
    else:
        integrated_secondary_fraction = 0.0

    if params["B0"] > 0.0:
        secondary_reservoir_converted = (
            converted_B
            / params["B0"]
        )
    else:
        secondary_reservoir_converted = 0.0

    # ========================================================
    # Characteristic times
    # ========================================================

    t_activation = activation_time(
        result,
        K=params["K"],
    )

    t_cross = crossover_time(
        result
    )

    t50 = conversion_time(
        result,
        P0=params["P0"],
        A0=params["A0"],
        B0=params["B0"],
        fraction=0.5,
    )

    t90 = conversion_time(
        result,
        P0=params["P0"],
        A0=params["A0"],
        B0=params["B0"],
        fraction=0.9,
    )

    if (
        np.isfinite(t50)
        and np.isfinite(t90)
    ):
        delta_t_50_90 = (
            t90 - t50
        )
    else:
        delta_t_50_90 = np.nan

    # ========================================================
    # State at t50 and t90
    # ========================================================

    state_50 = state_at_time(
        result,
        t50,
    )

    state_90 = state_at_time(
        result,
        t90,
    )

    # --------------------------------------------------------
    # Fraction of B remaining at t50
    # --------------------------------------------------------

    if (
        params["B0"] > 0.0
        and np.isfinite(state_50["B"])
    ):
        B50_fraction_remaining = (
            max(state_50["B"], 0.0)
            / params["B0"]
        )
    else:
        B50_fraction_remaining = np.nan

    # --------------------------------------------------------
    # Fraction of B remaining at t90
    # --------------------------------------------------------

    if (
        params["B0"] > 0.0
        and np.isfinite(state_90["B"])
    ):
        B90_fraction_remaining = (
            max(state_90["B"], 0.0)
            / params["B0"]
        )
    else:
        B90_fraction_remaining = np.nan

    # --------------------------------------------------------
    # Secondary-channel fraction at t50
    # --------------------------------------------------------

    total_rate_50 = (
        state_50["R_A"]
        + state_50["R_B"]
    )

    if (
        np.isfinite(total_rate_50)
        and total_rate_50 > 0.0
    ):
        secondary_fraction_at_t50 = (
            state_50["R_B"]
            / total_rate_50
        )
    else:
        secondary_fraction_at_t50 = np.nan

    # --------------------------------------------------------
    # Secondary-channel fraction at t90
    # --------------------------------------------------------

    total_rate_90 = (
        state_90["R_A"]
        + state_90["R_B"]
    )

    if (
        np.isfinite(total_rate_90)
        and total_rate_90 > 0.0
    ):
        secondary_fraction_at_t90 = (
            state_90["R_B"]
            / total_rate_90
        )
    else:
        secondary_fraction_at_t90 = np.nan

    # ========================================================
    # Analytical primary-limited reference time
    # ========================================================

    fraction_target = 0.9

    P_target_90 = (
        params["P0"]
        + fraction_target
        * (
            params["A0"]
            + params["B0"]
        )
    )

    # In the limiting case where the B reservoir is converted
    # sufficiently rapidly, the remaining amount needed to reach
    # P_target_90 is controlled only by A(t).
    A_target_90 = (
        initial_total
        - P_target_90
    )

    if (
        params["k_A"] > 0.0
        and params["A0"] > 0.0
        and A_target_90 > 0.0
        and A_target_90 < params["A0"]
    ):
        t90_primary_limit = (
            np.log(
                params["A0"]
                / A_target_90
            )
            / params["k_A"]
        )
    else:
        t90_primary_limit = np.nan

    # ========================================================
    # Delay relative to primary-limited reference
    # ========================================================

    if (
        np.isfinite(t90)
        and np.isfinite(t90_primary_limit)
    ):
        t90_excess_delay = (
            t90
            - t90_primary_limit
        )
    else:
        t90_excess_delay = np.nan

    # ========================================================
    # Return summary
    # ========================================================

    return {
        # ----------------------------------------------------
        # Input parameters
        # ----------------------------------------------------
        "P0": params["P0"],
        "A0": params["A0"],
        "B0": params["B0"],
        "k_A": params["k_A"],
        "k_B": params["k_B"],
        "K": params["K"],
        "n": params["n"],

        # ----------------------------------------------------
        # Characteristic times
        # ----------------------------------------------------
        "t_activation": t_activation,
        "t_cross": t_cross,
        "t50": t50,
        "t90": t90,
        "delta_t_50_90": delta_t_50_90,

        # Analytical reference
        "t90_primary_limit": t90_primary_limit,
        "t90_excess_delay": t90_excess_delay,

        # ----------------------------------------------------
        # Instantaneous channel relevance
        # ----------------------------------------------------
        "max_secondary_fraction": np.max(
            secondary_fraction
        ),

        "secondary_fraction_at_t50": (
            secondary_fraction_at_t50
        ),

        "secondary_fraction_at_t90": (
            secondary_fraction_at_t90
        ),

        # ----------------------------------------------------
        # Integrated channel relevance
        # ----------------------------------------------------
        "secondary_reservoir_converted": (
            secondary_reservoir_converted
        ),

        "integrated_secondary_fraction": (
            integrated_secondary_fraction
        ),

        # ----------------------------------------------------
        # Reservoir state at conversion milestones
        # ----------------------------------------------------
        "B50_fraction_remaining": (
            B50_fraction_remaining
        ),

        "B90_fraction_remaining": (
            B90_fraction_remaining
        ),

        # ----------------------------------------------------
        # Final state
        # ----------------------------------------------------
        "final_P": final_P,
        "final_A": final_A,
        "final_B": final_B,

        # ----------------------------------------------------
        # Numerical validation
        # ----------------------------------------------------
        "max_conservation_error": np.max(
            cons_error
        ),
    }


def run_parameter_sweep(
    grid,
    fixed_params,
    solver_kwargs=None,
):
    """
    Run a complete Cartesian parameter sweep.

    Parameters
    ----------
    grid : dict
        Parameters to vary.

    fixed_params : dict
        Model parameters held fixed.

    solver_kwargs : dict, optional
        Additional arguments passed to the numerical solver.

    Returns
    -------
    list of dict
        One summary dictionary per simulation.
    """

    if solver_kwargs is None:
        solver_kwargs = {}

    summaries = []

    runs = list(
        iter_parameter_grid(grid)
    )

    total = len(runs)

    for index, variable_params in enumerate(
        runs,
        start=1,
    ):

        params = {
            **fixed_params,
            **variable_params,
        }

        print(
            f"[{index}/{total}] "
            f"k_B={params['k_B']}, "
            f"K={params['K']}, "
            f"n={params['n']}"
        )

        result = solve_balance_system(
            **params,
            **solver_kwargs,
        )

        summary = summarize_run(
            result=result,
            params=params,
        )

        summaries.append(
            summary
        )

    return summaries