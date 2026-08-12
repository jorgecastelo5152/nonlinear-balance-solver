"""
Numerical integration routines for the nonlinear balance model.
"""

import numpy as np
from scipy.integrate import solve_ivp

from .model import activation, balance_equations


def solve_balance_system(
    P0=0.01,
    A0=0.39,
    B0=0.60,
    k_A=0.15,
    k_B=1.0,
    K=0.20,
    n=2,
    t_start=0.0,
    t_end=30.0,
    npoints=2000,
    rtol=1e-10,
    atol=1e-12,
    method="Radau",
):
    """
    Integrate the nonlinear balance system.

    Returns
    -------
    dict
        Time evolution and derived conversion rates.
    """

    y0 = [P0, A0, B0]

    t_eval = np.linspace(
        t_start,
        t_end,
        npoints,
    )

    sol = solve_ivp(
        balance_equations,
        (t_start, t_end),
        y0,
        args=(k_A, k_B, K, n),
        t_eval=t_eval,
        method=method,
        rtol=rtol,
        atol=atol,
    )

    if not sol.success:
        raise RuntimeError(
            f"ODE integration failed: {sol.message}"
        )

    t = sol.t
    P, A, B = sol.y

    activation_factor = activation(
        P=P,
        K=K,
        n=n,
    )

    R_A = k_A * A
    R_B = k_B * B * activation_factor

    return {
        "t": t,
        "P": P,
        "A": A,
        "B": B,
        "R_A": R_A,
        "R_B": R_B,
        "activation": activation_factor,
        "solution": sol,
    }