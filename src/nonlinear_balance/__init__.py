"""
Nonlinear Balance Solver.

Numerical tools for nonlinear coupled balance-equation systems.
"""

from .solver import solve_balance_system

__version__ = "0.1.0"

__all__ = [
    "solve_balance_system",
]