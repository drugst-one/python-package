"""
drugstone.task.scripts.make_upsetplot

This module implements the make_upset_plot function.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""

from upsetplot import from_contents, plot
from matplotlib import pyplot


def make_upset_plot(tasks: dict):
    """Opens a new window with an upset-plot of the results."""

    data = {}
    for t in tasks:
        data[t] = list(tasks[t]["results"]["drugs"].keys())

    d = from_contents(data)
    plot(d)
    pyplot.show()
