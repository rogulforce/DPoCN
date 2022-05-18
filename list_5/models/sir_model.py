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


def normalize_vector_length(u: np.array, v: np.array):
    normalizer = np.hypot(u, v)
    return u/normalizer, v/normalizer


def sir_model(Y: tuple[int | float , int | float, int | float], t: np.array, r: float, beta: float) -> tuple[float, float, float]:
    """ SIR model
    Args:
        Y = [S (int): suspectible, I (int | float): infected, R (int | float): removed]
        t (np.array): time (needed for odeint function)
        r (float): recovery rate
        beta (float): parameter of infectivity

    Returns:
        tuple[float, float, float]: derivatives of S, I and R
    """
    S, I, R = Y
    # print(I)
    # condition check
    if (not isinstance(S, (int, float))) or \
       (not isinstance(I, (int, float))) or \
       (not isinstance(R, (int, float))):
        raise ValueError("parameters S, I and R shall be int or float")
    elif (not isinstance(r, (int, float))) or (not 0 <= r):
        print(r)
        raise ValueError("r shall be float bigger than 0")
    elif not isinstance(beta, (int, float)):
        raise ValueError("beta shall be float")

    return dS_over_t(beta, S, I), dI_over_t(beta, S, I, r), dR_over_t(r, I)


def si_model(Y, t, r: float, beta: float) -> np.array:
    """ SI model
    Args:
        Y tuple[float | int, float | int]: S(flaot | int): suspectible, I (float | int): infected]
        t (np.array): time (needed for odeint function)
        r (float): recovery rate
        beta (float): parameter of infectivity

    Returns:
        np.array: dS/dt and dI/dt
    """
    S, I = Y

    # condition check
    if not isinstance(S, np.ndarray): # to make it available for vectors of starting conditions
        if (not isinstance(S, (int, float))) or (not isinstance(I, (int, float))):
            raise ValueError("parameters S, I and R shall be int")
        elif (not isinstance(r, (int, float))) or (not 0 <= r):
            raise ValueError("r shall be float >=0")
        elif not isinstance(beta, (int, float)):
            raise ValueError("beta shall be float")

    return np.array([dS_over_t(beta, S, I), dI_over_t(beta, S, I, r)])


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


def SIR_visualiser(solution, t, r, beta, S0, I0, R0):
    """ function visualising SIR model """
    S = solution[:, 0]
    I = solution[:, 1]
    R = solution[:, 2]

    theoretical_R0 = R_0(beta, r, S0)

    plt.figure(figsize=(14, 7))

    plt.plot(t, S, label="S(t)")
    plt.plot(t, I, label="I(t)")
    plt.plot(t, R, label="R(t)")
    plt.xlabel('t')
    plt.ylabel('N')
    plt.title(f'SIR model: beta={beta:.2f}, r={r:.2f}, \nS(0)={S0:.0f}, I(0)={I0:.0f}, R(0)={R0:.0f}\n'
              f'theoretical R_0={theoretical_R0:.2f}')
    plt.legend()
    plt.show()
    return


def phase_portrait_visualiser(solution, r, beta, S0, I0, R0, arrow_density=30):
    """ function creating phase portrait for numeric solution """
    S = solution[:, 0]
    I = solution[:, 1]

    theoretical_R0 = R_0(beta, r, S0)
    # create subset of S and I with bigger intervals
    S_t, I_t = np.meshgrid(np.linspace(min(S), max(S), arrow_density), np.linspace(min(I), max(I), arrow_density))
    # get derivatives
    dS_t, dI_t = si_model((S_t, I_t), 0, r, beta)
    dS_t, dI_t = normalize_vector_length(dS_t, dI_t)

    plt.figure(figsize=(7, 7))
    # plot
    plt.plot(S, I)
    # arrows
    plt.quiver(S_t, I_t, dS_t, dI_t)
    plt.xlabel('S(t)')
    plt.ylabel('I(t)')
    plt.title(f'phase portrait: beta={beta:.2f}, r={r:.2f}, \nS(0)={S0:.0f}, I(0)={I0:.0f}, R(0)={R0:.0f}\n'
              f'theoretical R_0={theoretical_R0:.2f}')
    return


def total_infected_vs_r0(t: np.array, S0: tuple, I0: tuple, R0: tuple, r: tuple, beta: tuple):
    n = len(S0)

    if  n != len(R0) != len(I0) != len(r) != len(beta):
        raise ValueError('initial conditions vectors shall have the same length!')

    total_infected_vector = []
    R0_vector = []

    for i in range(n):
        R0_th = R_0(beta[i], r[i], S0[i])
        R0_vector.append(R0_th)

        Y0 = (S0[i], I0[i], R0[i])
        solution = odeint(sir_model, Y0, t, args=(r[i], beta[i]))
        total_infected = max(solution[:, 2])
        total_infected_vector.append(total_infected)

    plt.figure(figsize=(14, 7))
    plt.scatter(R0_vector, total_infected_vector)
    plt.xlabel('R_0')
    plt.ylabel('total infected')
    plt.title(f'total_infected(R_0) : beta from {beta[0]:.2f} to {beta[-1]:.2f}, r from {r[0]:.2f} to {r[-1]:.2f}, '
               f'\nS(0)={S0[0]:.0f}, I(0)={I0[0]:.0f}, R(0)={R0[0]:.0f}')
    plt.show()
    return


# if __name__ == '__main__':
#     # t = np.arange(0, 30, 0.001)
#     # N = 100
#     #
#     # S0 = N
#     # I0 = 1
#     # R0 = 0
#     # Y0 = (N, I0, 0)
#     #
#     # for beta in [0.01, 0.02, 0.03]:
#     #     for r in [0.8, 1.2]:
#     #         solution = odeint(sir_model, Y0, t, args=(r, beta))
#     #
#     #         SIR_visualiser(solution, t, r, beta, N, I0, 0)
#     #         phase_portrait_visualiser(solution, r, beta, N, I0, 0)
#
#     t = np.arange(0, 30, 0.5)
#     S0 = [100] * 9
#     I0 = [1] * 9
#     R0 = [0] * 9
#     beta = [0.01] * 9
#     r = [0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3]
#     total_infected_vs_r0(t,S0,I0,R0,r,beta)
#
#     beta = [0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13]
#     r = [0.01] * 9
#     total_infected_vs_r0(t, S0, I0, R0, r, beta)