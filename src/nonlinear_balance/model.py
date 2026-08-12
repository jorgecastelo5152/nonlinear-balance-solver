"""
Mathematical model for the nonlinear coupled balance system.
"""


def activation(P, K, n):
    """
    Hill-type nonlinear activation function.

    Parameters
    ----------
    P : float or array-like
        Accumulated product.
    K : float
        Characteristic activation scale.
    n : float
        Hill exponent.

    Returns
    -------
    float or array-like
        Activation factor between 0 and 1.
    """
    return P**n / (K**n + P**n)


def reaction_rates(P, A, B, k_A, k_B, K, n):
    """
    Compute the conversion rates of the two reservoirs.
    """

    R_A = k_A * A
    R_B = k_B * B * activation(P, K, n)

    return R_A, R_B


def balance_equations(t, y, k_A, k_B, K, n):
    """
    Coupled nonlinear balance equations.

    State vector
    ------------
    y = [P, A, B]

    Equations
    ---------
    dP/dt = R_A + R_B
    dA/dt = -R_A
    dB/dt = -R_B
    """

    P, A, B = y

    R_A, R_B = reaction_rates(
        P=P,
        A=A,
        B=B,
        k_A=k_A,
        k_B=k_B,
        K=K,
        n=n,
    )

    return [
        R_A + R_B,
        -R_A,
        -R_B,
    ]