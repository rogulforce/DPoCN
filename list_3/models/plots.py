# all the functions in this file were prepared for other course with Bogna Jaszczak who is co-owner of 4 first functions
# below.

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
from list_3.models.utils import show_statistics


def pdf_emp(data: np.array, bins: int = 100, show: bool = False, **kwargs) -> None:
    """ function plotting a histogram of the given data.
    Args:
        data (np.array): given data
        bins (int): bins of the histogram
        show (bool): show indicator. Defaults to None.
        **kwargs: Optional arguments for matplotlib.pyplot.histogram() function
    Returns:
        None
    """
    plt.hist(data, bins=bins, density=True, **kwargs)
    if show:
        plt.show()


def cdf_emp(data: np.array, show: bool = False, **kwargs) -> None:
    """ function plotting a CDF of the given data.
    Args:
        data (np.array): given data
        show (bool): show indicator. Defaults to None.
        **kwargs: Optional arguments for matplotlib.pyplot.plot() function
    Returns:
        None
    """
    data.sort()
    y = np.arange(len(data))/float(len(data))

    plt.plot(data, y, 'b-', **kwargs)
    if show:
        plt.show()


def dist_cdf_plot(domain: tuple = (-4, 4), distribution=scipy.stats.norm, show: bool = False, **kwargs) -> None:
    """ function plotting a CDF of the given distribution.
    Args:
        domain (tuple): domain of the distribution.
        distribution: scipy.stats theoretical distribution. Defaults to scipy.stats.norm.
        show (bool): show indicator. Defaults to None.
        **kwargs: Optional arguments for the distribution.
    Returns:
        None
    """
    x = np.linspace(domain[0], domain[1], 1000)
    plt.plot(x, distribution.cdf(x, **kwargs), 'r.')
    if show:
        plt.show()


def dist_pdf_plot(domain: tuple = (-4, 4), distribution=scipy.stats.norm, show: bool = False, **kwargs) -> None:
    """ function plotting a PDF of the given distribution.
    Args:
        domain (tuple): domain of the distribution.
        distribution: scipy.stats theoretical distribution. Defaults to scipy.stats.norm.
        show (bool): show indicator. Defaults to None.
        **kwargs: Optional arguments for the distribution.
    Returns:
        None
    """
    x = np.linspace(domain[0], domain[1], 1000)
    plt.plot(x, distribution.pdf(x, **kwargs), 'r.')
    if show:
        plt.show()


def show_degree_distribution(network, distribution=None):

    stats = show_statistics(network)
    print(f'statistics: {stats}')

    degree_list = [val for key, val in network.degree()]
    domain_start, domain_end = min(degree_list), max(degree_list)
    plt.figure(0)
    plt.xlabel('x')
    plt.ylabel('pdf')
    pdf_emp(degree_list, bins=domain_end - domain_start)

    # fit distribution
    if distribution:
        dist_pdf_plot(domain=(domain_start, domain_end), distribution=scipy.stats.norm, loc=stats['mean_degree'],
                      scale=np.sqrt(stats['var_degree']), show=True)
    else:
        plt.show()

    plt.figure(1)
    plt.xlim(domain_start, domain_end)
    plt.xlabel('x')
    plt.ylabel('cdf')
    if distribution:
        dist_cdf_plot(domain=(domain_start, domain_end), distribution=scipy.stats.norm, loc=stats['mean_degree'],
                      scale=np.sqrt(stats['var_degree']))
    cdf_emp(degree_list, show=True)
