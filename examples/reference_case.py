#!/usr/bin/env python3

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from nonlinear_balance import solve_balance_system

from nonlinear_balance.analysis import (
    analytical_control_solution,
    conservation_error,
    activation_time,
    crossover_time,
    control_errors,
)

from nonlinear_balance.plotting import (
    plot_evolution,
    plot_rates,
    plot_activation,
)


# ============================================================
# Reference configuration
# ============================================================

params = {
    "P0": 0.01,
    "A0": 0.39,
    "B0": 0.60,
    "k_A": 0.15,
    "k_B": 1.0,
    "K": 0.20,
    "n": 2,
}


# ============================================================
# Full nonlinear model
# ============================================================

result = solve_balance_system(
    **params
)


# ============================================================
# Conservation diagnostic
# ============================================================

initial_total = (
    params["P0"]
    + params["A0"]
    + params["B0"]
)

cons_error = conservation_error(
    result,
    initial_total=initial_total,
)

print()
print("=== Numerical diagnostics ===")

print(
    "Maximum conservation error: "
    f"{np.max(cons_error):.3e}"
)

print(
    f"Minimum P: {np.min(result['P']):.6e}"
)

print(
    f"Minimum A: {np.min(result['A']):.6e}"
)

print(
    f"Minimum B: {np.min(result['B']):.6e}"
)


# ============================================================
# Control model
# ============================================================

control_params = dict(params)
control_params["k_B"] = 0.0

control = solve_balance_system(
    **control_params
)

analytical = analytical_control_solution(
    t=control["t"],
    P0=params["P0"],
    A0=params["A0"],
    B0=params["B0"],
    k_A=params["k_A"],
)

errors = control_errors(
    numerical=control,
    analytical=analytical,
)

print()
print("=== Control-model validation ===")

print(
    f"Max |P_num - P_exact|: "
    f"{errors['P']:.3e}"
)

print(
    f"Max |A_num - A_exact|: "
    f"{errors['A']:.3e}"
)

print(
    f"Max |B_num - B_exact|: "
    f"{errors['B']:.3e}"
)


# ============================================================
# Characteristic times
# ============================================================

t_act = activation_time(
    result,
    K=params["K"],
)

t_cross = crossover_time(
    result
)

print()
print("=== Characteristic times ===")

print(
    f"Activation time P = K: "
    f"{t_act:.6f}"
)

print(
    f"Secondary channel overtakes primary: "
    f"{t_cross:.6f}"
)


# ============================================================
# Figures
# ============================================================

# ============================================================
# Figures
# ============================================================

from pathlib import Path

figure_dir = Path("figures")
figure_dir.mkdir(exist_ok=True)

fig_evolution = plot_evolution(result)
fig_rates = plot_rates(result)
fig_activation = plot_activation(result)

fig_evolution.savefig(
    figure_dir / "reference_evolution.png",
    dpi=200,
    bbox_inches="tight",
)

fig_rates.savefig(
    figure_dir / "reference_rates.png",
    dpi=200,
    bbox_inches="tight",
)

fig_activation.savefig(
    figure_dir / "reference_activation.png",
    dpi=200,
    bbox_inches="tight",
)

print()
print("=== Figures ===")
print("Saved: figures/reference_evolution.png")
print("Saved: figures/reference_rates.png")
print("Saved: figures/reference_activation.png")

plt.show()