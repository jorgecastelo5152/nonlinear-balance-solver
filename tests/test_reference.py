import numpy as np

from nonlinear_balance import solve_balance_system

from nonlinear_balance.analysis import (
    analytical_control_solution,
    conservation_error,
    activation_time,
    crossover_time,
)


def test_conservation():
    result = solve_balance_system()

    error = conservation_error(
        result,
        initial_total=1.0,
    )

    assert np.max(error) < 1e-10


def test_control_solution():
    result = solve_balance_system(
        k_B=0.0
    )

    exact = analytical_control_solution(
        t=result["t"],
        P0=0.01,
        A0=0.39,
        B0=0.60,
        k_A=0.15,
    )

    assert np.max(
        np.abs(result["P"] - exact["P"])
    ) < 1e-9

    assert np.max(
        np.abs(result["A"] - exact["A"])
    ) < 1e-9

    assert np.max(
        np.abs(result["B"] - exact["B"])
    ) < 1e-12


def test_positivity():
    result = solve_balance_system()

    assert np.min(result["P"]) >= 0.0
    assert np.min(result["A"]) >= 0.0
    assert np.min(result["B"]) >= 0.0


def test_reference_times():
    result = solve_balance_system()

    t_act = activation_time(
        result,
        K=0.20,
    )

    t_cross = crossover_time(
        result
    )

    assert np.isfinite(t_act)
    assert np.isfinite(t_cross)

    assert t_cross < t_act