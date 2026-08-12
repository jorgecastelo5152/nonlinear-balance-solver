#!/usr/bin/env python3

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# Input
# ============================================================

results_file = Path("results/parameter_sweep.csv")

if not results_file.exists():
    raise FileNotFoundError(
        f"Could not find {results_file}. "
        "Run examples/parameter_sweep.py first."
    )


# ============================================================
# Load sweep
# ============================================================

df = pd.read_csv(results_file)

print()
print("=== Parameter sweep overview ===")
print(f"Number of simulations: {len(df)}")


# ============================================================
# Parameter-space information
# ============================================================

print()
print("=== Parameter values ===")

for parameter in ["k_B", "K", "n"]:

    values = np.sort(
        df[parameter].unique()
    )

    print(
        f"{parameter}: {values}"
    )


# ============================================================
# Missing characteristic times
# ============================================================

time_columns = [
    "t_activation",
    "t_cross",
    "t50",
    "t90",
]

print()
print("=== Characteristic-time availability ===")

for column in time_columns:

    missing = df[column].isna().sum()

    print(
        f"{column}: "
        f"{missing}/{len(df)} missing"
    )


# ============================================================
# Observable ranges
# ============================================================

columns_to_summarize = [
    "t_activation",
    "t_cross",
    "t50",
    "t90",
    "delta_t_50_90",
    "t90_primary_limit",
    "t90_excess_delay",
    "B50_fraction_remaining",
    "B90_fraction_remaining",
    "secondary_fraction_at_t50",
    "secondary_fraction_at_t90",
    "secondary_reservoir_converted",
    "integrated_secondary_fraction",
    "max_secondary_fraction",
    "final_P",
    "final_B",
    "max_conservation_error",
]

print()
print("=== Observable ranges ===")

for column in columns_to_summarize:

    values = df[column].dropna()

    print()
    print(column)

    if len(values) == 0:
        print("  no finite values")
        continue

    print(
        f"  min    = {values.min():.6g}"
    )

    print(
        f"  q25    = {values.quantile(0.25):.6g}"
    )

    print(
        f"  median = {values.median():.6g}"
    )

    print(
        f"  q75    = {values.quantile(0.75):.6g}"
    )

    print(
        f"  mean   = {values.mean():.6g}"
    )

    print(
        f"  max    = {values.max():.6g}"
    )


# ============================================================
# Activation versus secondary dominance
# ============================================================

valid_times = df[
    df["t_activation"].notna()
    & df["t_cross"].notna()
].copy()

valid_times["delta_activation_cross"] = (
    valid_times["t_activation"]
    - valid_times["t_cross"]
)

print()
print("=== Activation versus secondary dominance ===")

print(
    "Cases with both characteristic times: "
    f"{len(valid_times)}"
)

if len(valid_times) > 0:

    n_cross_before_activation = (
        valid_times["delta_activation_cross"] > 0
    ).sum()

    n_activation_before_cross = (
        valid_times["delta_activation_cross"] < 0
    ).sum()

    n_equal = (
        np.isclose(
            valid_times["delta_activation_cross"],
            0.0,
        )
    ).sum()

    print(
        "Secondary dominance before P = K: "
        f"{n_cross_before_activation}"
    )

    print(
        "P = K before secondary dominance: "
        f"{n_activation_before_cross}"
    )

    print(
        "Approximately simultaneous: "
        f"{n_equal}"
    )

    print(
        "delta range: "
        f"{valid_times['delta_activation_cross'].min():.4f}"
        " to "
        f"{valid_times['delta_activation_cross'].max():.4f}"
    )


# ============================================================
# Conversion-speed diagnostics
# ============================================================

valid_conversion = df[
    df["t50"].notna()
    & df["t90"].notna()
].copy()

print()
print("=== Conversion-speed diagnostics ===")

print(
    "Cases reaching both 50% and 90% conversion: "
    f"{len(valid_conversion)}"
)

if len(valid_conversion) > 0:

    print(
        "Fastest t50: "
        f"{valid_conversion['t50'].min():.4f}"
    )

    print(
        "Slowest t50: "
        f"{valid_conversion['t50'].max():.4f}"
    )

    print(
        "Fastest t90: "
        f"{valid_conversion['t90'].min():.4f}"
    )

    print(
        "Slowest t90: "
        f"{valid_conversion['t90'].max():.4f}"
    )

    print(
        "delta_t_50_90 range: "
        f"{valid_conversion['delta_t_50_90'].min():.4f}"
        " to "
        f"{valid_conversion['delta_t_50_90'].max():.4f}"
    )


# ============================================================
# Extreme cases: fastest conversion
# ============================================================

print()
print("=== Fastest conversions ===")

fastest = (
    df.sort_values(
        "t90",
        ascending=True,
        na_position="last",
    )
    .head(10)
)

print(
    fastest[
        [
            "k_B",
            "K",
            "n",
            "t50",
            "t90",
            "delta_t_50_90",
            "integrated_secondary_fraction",
            "secondary_reservoir_converted",
        ]
    ].to_string(index=False)
)


# ============================================================
# Extreme cases: slowest conversion
# ============================================================

print()
print("=== Slowest conversions ===")

slowest = (
    df.sort_values(
        "t90",
        ascending=False,
        na_position="last",
    )
    .head(10)
)

print(
    slowest[
        [
            "k_B",
            "K",
            "n",
            "t50",
            "t90",
            "delta_t_50_90",
            "integrated_secondary_fraction",
            "secondary_reservoir_converted",
        ]
    ].to_string(index=False)
)


# ============================================================
# Extreme cases: integrated secondary contribution
# ============================================================

print()
print("=== Largest integrated secondary contributions ===")

secondary_high = (
    df.sort_values(
        "integrated_secondary_fraction",
        ascending=False,
    )
    .head(10)
)

print(
    secondary_high[
        [
            "k_B",
            "K",
            "n",
            "integrated_secondary_fraction",
            "secondary_reservoir_converted",
            "t_cross",
            "t90",
        ]
    ].to_string(index=False)
)


print()
print("=== Smallest integrated secondary contributions ===")

secondary_low = (
    df.sort_values(
        "integrated_secondary_fraction",
        ascending=True,
    )
    .head(10)
)

print(
    secondary_low[
        [
            "k_B",
            "K",
            "n",
            "integrated_secondary_fraction",
            "secondary_reservoir_converted",
            "t_cross",
            "t90",
        ]
    ].to_string(index=False)
)


# ============================================================
# Figure directory
# ============================================================

figure_dir = Path(
    "figures/sweep_exploration"
)

figure_dir.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# Histogram: t90
# ============================================================

fig, ax = plt.subplots(
    figsize=(7, 5)
)

ax.hist(
    df["t90"].dropna(),
    bins=15,
)

ax.set_xlabel(
    r"$t_{90}$"
)

ax.set_ylabel(
    "Number of simulations"
)

ax.grid(
    True,
    linestyle=":",
)

fig.tight_layout()

fig.savefig(
    figure_dir / "t90_histogram.png",
    dpi=200,
    bbox_inches="tight",
)


# ============================================================
# Histogram: integrated secondary contribution
# ============================================================

fig, ax = plt.subplots(
    figsize=(7, 5)
)

ax.hist(
    df["integrated_secondary_fraction"],
    bins=15,
)

ax.set_xlabel(
    "Integrated secondary-channel fraction"
)

ax.set_ylabel(
    "Number of simulations"
)

ax.grid(
    True,
    linestyle=":",
)

fig.tight_layout()

fig.savefig(
    figure_dir
    / "integrated_secondary_fraction_histogram.png",
    dpi=200,
    bbox_inches="tight",
)


# ============================================================
# Histogram: secondary reservoir conversion
# ============================================================

fig, ax = plt.subplots(
    figsize=(7, 5)
)

ax.hist(
    df["secondary_reservoir_converted"],
    bins=15,
)

ax.set_xlabel(
    "Fraction of secondary reservoir converted"
)

ax.set_ylabel(
    "Number of simulations"
)

ax.grid(
    True,
    linestyle=":",
)

fig.tight_layout()

fig.savefig(
    figure_dir
    / "secondary_reservoir_conversion_histogram.png",
    dpi=200,
    bbox_inches="tight",
)


# ============================================================
# Activation time versus crossover time
# ============================================================

fig, ax = plt.subplots(
    figsize=(6, 6)
)

ax.scatter(
    valid_times["t_activation"],
    valid_times["t_cross"],
)

if len(valid_times) > 0:

    min_time = min(
        valid_times["t_activation"].min(),
        valid_times["t_cross"].min(),
    )

    max_time = max(
        valid_times["t_activation"].max(),
        valid_times["t_cross"].max(),
    )

    ax.plot(
        [min_time, max_time],
        [min_time, max_time],
        linestyle=":",
    )

ax.set_xlabel(
    r"Activation time $t_{\rm act}$"
)

ax.set_ylabel(
    r"Crossover time $t_{\rm cross}$"
)

ax.grid(
    True,
    linestyle=":",
)

fig.tight_layout()

fig.savefig(
    figure_dir
    / "activation_vs_crossover.png",
    dpi=200,
    bbox_inches="tight",
)


# ============================================================
# t50 versus t90
# ============================================================

fig, ax = plt.subplots(
    figsize=(6, 6)
)

ax.scatter(
    valid_conversion["t50"],
    valid_conversion["t90"],
)

ax.set_xlabel(
    r"$t_{50}$"
)

ax.set_ylabel(
    r"$t_{90}$"
)

ax.grid(
    True,
    linestyle=":",
)

fig.tight_layout()

fig.savefig(
    figure_dir / "t50_vs_t90.png",
    dpi=200,
    bbox_inches="tight",
)


# ============================================================
# Integrated secondary fraction versus t90
# ============================================================

valid_t90 = df[
    df["t90"].notna()
].copy()

fig, ax = plt.subplots(
    figsize=(7, 5)
)

ax.scatter(
    valid_t90["integrated_secondary_fraction"],
    valid_t90["t90"],
)

ax.set_xlabel(
    "Integrated secondary-channel fraction"
)

ax.set_ylabel(
    r"$t_{90}$"
)

ax.grid(
    True,
    linestyle=":",
)

fig.tight_layout()

fig.savefig(
    figure_dir
    / "integrated_secondary_fraction_vs_t90.png",
    dpi=200,
    bbox_inches="tight",
)


# ============================================================
# k_B dependence of t90
# ============================================================

fig, ax = plt.subplots(
    figsize=(7, 5)
)

for n_value in sorted(
    df["n"].unique()
):

    subset = df[
        df["n"] == n_value
    ]

    grouped = (
        subset
        .groupby("k_B")["t90"]
        .mean()
    )

    ax.plot(
        grouped.index,
        grouped.values,
        marker="o",
        label=rf"$n={n_value:g}$",
    )

ax.set_xlabel(
    r"$k_B$"
)

ax.set_ylabel(
    r"Mean $t_{90}$"
)

ax.legend()

ax.grid(
    True,
    linestyle=":",
)

fig.tight_layout()

fig.savefig(
    figure_dir
    / "t90_vs_kB.png",
    dpi=200,
    bbox_inches="tight",
)


# ============================================================
# K dependence of t90
# ============================================================

fig, ax = plt.subplots(
    figsize=(7, 5)
)

for n_value in sorted(
    df["n"].unique()
):

    subset = df[
        df["n"] == n_value
    ]

    grouped = (
        subset
        .groupby("K")["t90"]
        .mean()
    )

    ax.plot(
        grouped.index,
        grouped.values,
        marker="o",
        label=rf"$n={n_value:g}$",
    )

ax.set_xlabel(
    r"$K$"
)

ax.set_ylabel(
    r"Mean $t_{90}$"
)

ax.legend()

ax.grid(
    True,
    linestyle=":",
)

fig.tight_layout()

fig.savefig(
    figure_dir
    / "t90_vs_K.png",
    dpi=200,
    bbox_inches="tight",
)


# ============================================================
# k_B dependence of integrated secondary contribution
# ============================================================

fig, ax = plt.subplots(
    figsize=(7, 5)
)

for n_value in sorted(
    df["n"].unique()
):

    subset = df[
        df["n"] == n_value
    ]

    grouped = (
        subset
        .groupby("k_B")[
            "integrated_secondary_fraction"
        ]
        .mean()
    )

    ax.plot(
        grouped.index,
        grouped.values,
        marker="o",
        label=rf"$n={n_value:g}$",
    )

ax.set_xlabel(
    r"$k_B$"
)

ax.set_ylabel(
    "Mean integrated secondary fraction"
)

ax.legend()

ax.grid(
    True,
    linestyle=":",
)

fig.tight_layout()

fig.savefig(
    figure_dir
    / "integrated_secondary_fraction_vs_kB.png",
    dpi=200,
    bbox_inches="tight",
)


# ============================================================
# K dependence of integrated secondary contribution
# ============================================================

fig, ax = plt.subplots(
    figsize=(7, 5)
)

for n_value in sorted(
    df["n"].unique()
):

    subset = df[
        df["n"] == n_value
    ]

    grouped = (
        subset
        .groupby("K")[
            "integrated_secondary_fraction"
        ]
        .mean()
    )

    ax.plot(
        grouped.index,
        grouped.values,
        marker="o",
        label=rf"$n={n_value:g}$",
    )

ax.set_xlabel(
    r"$K$"
)

ax.set_ylabel(
    "Mean integrated secondary fraction"
)

ax.legend()

ax.grid(
    True,
    linestyle=":",
)

fig.tight_layout()

fig.savefig(
    figure_dir
    / "integrated_secondary_fraction_vs_K.png",
    dpi=200,
    bbox_inches="tight",
)



# ============================================================
# Aggregate behaviour by k_B
# ============================================================

print()
print("=== Median behaviour by k_B ===")

summary_by_kB = (
    df.groupby("k_B")[
        [
            "t_activation",
            "t_cross",
            "t50",
            "t90",
            "delta_t_50_90",
            "secondary_reservoir_converted",
            "integrated_secondary_fraction",
        ]
    ]
    .median()
)

print(
    summary_by_kB.to_string()
)

# ============================================================
# Aggregate behaviour by K
# ============================================================

print()
print("=== Median behaviour by K ===")

summary_by_K = (
    df.groupby("K")[
        [
            "t_activation",
            "t_cross",
            "t50",
            "t90",
            "delta_t_50_90",
            "secondary_reservoir_converted",
            "integrated_secondary_fraction",
        ]
    ]
    .median()
)

print(
    summary_by_K.to_string()
)

# ============================================================
# Aggregate behaviour by n
# ============================================================

print()
print("=== Median behaviour by n ===")

summary_by_n = (
    df.groupby("n")[
        [
            "t_activation",
            "t_cross",
            "t50",
            "t90",
            "delta_t_50_90",
            "secondary_reservoir_converted",
            "integrated_secondary_fraction",
        ]
    ]
    .median()
)

print(
    summary_by_n.to_string()
)

# ============================================================
# Primary-limited reference analysis
# ============================================================

valid_t90_reference = df[
    df["t90"].notna()
    & df["t90_primary_limit"].notna()
].copy()

print()
print("=== Delay relative to primary-limited reference ===")

print(
    "Cases reaching t90: "
    f"{len(valid_t90_reference)}/{len(df)}"
)

if len(valid_t90_reference) > 0:

    print(
        "Primary-limited reference time: "
        f"{valid_t90_reference['t90_primary_limit'].iloc[0]:.6f}"
    )

    print(
        "Minimum excess delay: "
        f"{valid_t90_reference['t90_excess_delay'].min():.6f}"
    )

    print(
        "Median excess delay: "
        f"{valid_t90_reference['t90_excess_delay'].median():.6f}"
    )

    print(
        "Maximum excess delay: "
        f"{valid_t90_reference['t90_excess_delay'].max():.6f}"
    )


# ============================================================
# Reservoir state at t50 and t90
# ============================================================

print()
print("=== Secondary reservoir at conversion milestones ===")

for column in [
    "B50_fraction_remaining",
    "B90_fraction_remaining",
]:

    values = df[column].dropna()

    print()
    print(column)

    print(
        f"  min    = {values.min():.6g}"
    )

    print(
        f"  q25    = {values.quantile(0.25):.6g}"
    )

    print(
        f"  median = {values.median():.6g}"
    )

    print(
        f"  q75    = {values.quantile(0.75):.6g}"
    )

    print(
        f"  max    = {values.max():.6g}"
    )


# ============================================================
# Secondary-channel activity at conversion milestones
# ============================================================

print()
print("=== Secondary-channel activity at milestones ===")

for column in [
    "secondary_fraction_at_t50",
    "secondary_fraction_at_t90",
]:

    values = df[column].dropna()

    print()
    print(column)

    print(
        f"  min    = {values.min():.6g}"
    )

    print(
        f"  q25    = {values.quantile(0.25):.6g}"
    )

    print(
        f"  median = {values.median():.6g}"
    )

    print(
        f"  q75    = {values.quantile(0.75):.6g}"
    )

    print(
        f"  max    = {values.max():.6g}"
    )


# ============================================================
# Largest secondary-induced delays
# ============================================================

print()
print("=== Largest delays relative to primary limit ===")

largest_delays = (
    valid_t90_reference
    .sort_values(
        "t90_excess_delay",
        ascending=False,
    )
    .head(15)
)

print(
    largest_delays[
        [
            "k_B",
            "K",
            "n",
            "t90",
            "t90_primary_limit",
            "t90_excess_delay",
            "B90_fraction_remaining",
            "secondary_fraction_at_t90",
        ]
    ].to_string(index=False)
)


# ============================================================
# Smallest secondary-induced delays
# ============================================================

print()
print("=== Smallest delays relative to primary limit ===")

smallest_delays = (
    valid_t90_reference
    .sort_values(
        "t90_excess_delay",
        ascending=True,
    )
    .head(15)
)

print(
    smallest_delays[
        [
            "k_B",
            "K",
            "n",
            "t90",
            "t90_primary_limit",
            "t90_excess_delay",
            "B90_fraction_remaining",
            "secondary_fraction_at_t90",
        ]
    ].to_string(index=False)
)






# ============================================================
# Histogram: excess delay relative to primary limit
# ============================================================

fig, ax = plt.subplots(
    figsize=(7, 5)
)

ax.hist(
    valid_t90_reference["t90_excess_delay"],
    bins=15,
)

ax.set_xlabel(
    r"$t_{90}-t_{90}^{\rm primary}$"
)

ax.set_ylabel(
    "Number of simulations"
)

ax.grid(
    True,
    linestyle=":",
)

fig.tight_layout()

fig.savefig(
    figure_dir / "t90_excess_delay_histogram.png",
    dpi=200,
    bbox_inches="tight",
)





# ============================================================
# Excess delay versus B remaining at t90
# ============================================================

fig, ax = plt.subplots(
    figsize=(7, 5)
)

ax.scatter(
    valid_t90_reference["B90_fraction_remaining"],
    valid_t90_reference["t90_excess_delay"],
)

ax.set_xlabel(
    r"$B(t_{90})/B_0$"
)

ax.set_ylabel(
    r"$t_{90}-t_{90}^{\rm primary}$"
)

ax.grid(
    True,
    linestyle=":",
)

fig.tight_layout()

fig.savefig(
    figure_dir
    / "t90_excess_delay_vs_B90_remaining.png",
    dpi=200,
    bbox_inches="tight",
)



# ============================================================
# B remaining at t50 versus B remaining at t90
# ============================================================

valid_B_milestones = df[
    df["B50_fraction_remaining"].notna()
    & df["B90_fraction_remaining"].notna()
].copy()

fig, ax = plt.subplots(
    figsize=(6, 6)
)

ax.scatter(
    valid_B_milestones["B50_fraction_remaining"],
    valid_B_milestones["B90_fraction_remaining"],
)

ax.set_xlabel(
    r"$B(t_{50})/B_0$"
)

ax.set_ylabel(
    r"$B(t_{90})/B_0$"
)

ax.grid(
    True,
    linestyle=":",
)

fig.tight_layout()

fig.savefig(
    figure_dir
    / "B50_vs_B90_remaining.png",
    dpi=200,
    bbox_inches="tight",
)














# ============================================================
# Finish
# ============================================================

print()
print(
    "Exploratory figures saved in "
    f"{figure_dir}"
)

plt.show()