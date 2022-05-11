from typing import Optional

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


def dS_over_t(beta, S, I):
    return -1 * beta * S * I


def dI_over_t(beta, S, I, r):
    return beta * S * I - r * I


def dR_over_t(r, I):
    return r * I


def R_0(beta, r, N):
    return beta*N/r


def sir_model(Y: tuple[int,int,int], t: np.array, r: float, beta: float) -> tuple[float, float, float]:
    """
    Args:
        Y = [S (int): suspectible, I (int): infected, R (int): removed]
        t (np.array): time (needed for odeint function)
        r (float): recovery rate
        beta (float): parameter of infectivity

    Returns:
        tuple[float, float, float]: derivatives of S, I and R
    """
    S, I, R = Y
    # condition check
    if (not isinstance(S, (int, float))) or \
       (not isinstance(I, (int, float))) or \
       (not isinstance(R, (int, float))):
        raise ValueError("parameters S, I and R shall be int or float")
    elif (not isinstance(r, (int, float))) or (not 0 <= r):
        raise ValueError("r shall be float from 0 to 1")
    elif not isinstance(beta, (int, float)):
        raise ValueError("beta shall be float")

    return dS_over_t(beta, S, I), dI_over_t(beta, S, I, r), dR_over_t(r, I)


def si_model(Y: tuple[float | int, float | int], t, r: float, beta: float) -> tuple[float, float]:
    """
    Args:
        Y = [S (float | int): suspectible, I (int): infected]
        t (np.array): time (needed for odeint function)
        r (float): recovery rate
        beta (float): parameter of infectivity

    Returns:
        tuple[float, float]: dS/dt and dI/dt
    """
    S, I = Y

    # condition check
    if (not isinstance(S, (int, float))) or (not isinstance(I, (int, float))):
        raise ValueError("parameters S, I and R shall be int")
    elif (not isinstance(r, (int, float))) or (not 0 <= r):
        raise ValueError("r shall be float >=0")
    elif not isinstance(beta, (int, float)):
        raise ValueError("beta shall be float")

    return dS_over_t(beta, S, I), dI_over_t(beta, S, I, r)


def solver(model: callable, Y_0: tuple[int, int, Optional[int]], t: np.array, r: float, beta: float):
    """ sovler of the system of equations
    Args:
        model (callable): function (basically SI or SIR model)
        Y_0 (tuple[int, int, Optional[int]]): initial conditions of S, I (and optional R for SIR model)
        t (np.array): time
        r (float): function parameter
        beta (float): function parameter
    Returns:

    """
    return odeint(model, Y_0, t, args=(r, beta))


def SIR_visualiser(solution, r, beta, S_0, I_0, R_0):
    plt.figure()


def phase_portrait_visualiser(solution, r, beta, S_0, I_0):
    plt.figure()




