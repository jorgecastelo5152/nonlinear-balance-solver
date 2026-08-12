#!/usr/bin/env python3

from pathlib import Path

import pandas as pd

from nonlinear_balance.sweep import (
    run_parameter_sweep,
)


# ============================================================
# Fixed reference parameters
# ============================================================

fixed_params = {
    "P0": 0.01,
    "A0": 0.39,
    "B0": 0.60,
    "k_A": 0.15,
}


# ============================================================
# Parameter grid
# ============================================================

grid = {
    "k_B": [
        0.1,
        0.3,
        0.6,
        1.0,
        2.0,
        3.0,
    ],

    "K": [
        0.05,
        0.10,
        0.20,
        0.30,
        0.50,
    ],

    "n": [
        1,
        2,
        4,
    ],
}


# ============================================================
# Solver configuration
# ============================================================

solver_kwargs = {
    "t_start": 0.0,
    "t_end": 30.0,
    "npoints": 2000,
    "rtol": 1e-10,
    "atol": 1e-12,
    "method": "Radau",
}


# ============================================================
# Run sweep
# ============================================================

summaries = run_parameter_sweep(
    grid=grid,
    fixed_params=fixed_params,
    solver_kwargs=solver_kwargs,
)


# ============================================================
# Convert to table
# ============================================================

df = pd.DataFrame(summaries)


# ============================================================
# Save results
# ============================================================

results_dir = Path("results")
results_dir.mkdir(exist_ok=True)

output_file = (
    results_dir
    / "parameter_sweep.csv"
)

df.to_csv(
    output_file,
    index=False,
)

print()
print(
    f"Saved {len(df)} simulations to "
    f"{output_file}"
)

print()
print(df.head())