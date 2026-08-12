"""
Visualization tools for nonlinear balance simulations.
"""

import matplotlib.pyplot as plt


def plot_evolution(result):
    """
    Plot P, A and B as functions of time.
    """

    t = result["t"]

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(
        t,
        result["P"],
        label="Product P",
    )

    ax.plot(
        t,
        result["A"],
        label="Reservoir A",
        linestyle="--",
    )

    ax.plot(
        t,
        result["B"],
        label="Reservoir B",
        linestyle=":",
    )

    ax.set_xlabel("Dimensionless time")
    ax.set_ylabel("Normalized quantity")

    ax.legend()
    ax.grid(True, linestyle=":")

    fig.tight_layout()

    return fig


def plot_rates(result):
    """
    Plot the two conversion rates.
    """

    t = result["t"]

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(
        t,
        result["R_A"],
        label=r"$R_A$",
    )

    ax.plot(
        t,
        result["R_B"],
        label=r"$R_B$",
        linestyle="--",
    )

    ax.set_xlabel("Dimensionless time")
    ax.set_ylabel("Conversion rate")

    ax.legend()
    ax.grid(True, linestyle=":")

    fig.tight_layout()

    return fig


def plot_activation(result):
    """
    Plot the nonlinear activation factor.
    """

    t = result["t"]

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(
        t,
        result["activation"],
        label=r"$f(P)$",
    )

    ax.axhline(
        0.5,
        linestyle=":",
        label=r"$f(P)=1/2$",
    )

    ax.set_xlabel("Dimensionless time")
    ax.set_ylabel(r"Activation $f(P)$")

    ax.set_ylim(0.0, 1.05)

    ax.legend()
    ax.grid(True, linestyle=":")

    fig.tight_layout()

    return fig