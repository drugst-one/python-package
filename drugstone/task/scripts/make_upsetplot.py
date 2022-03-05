from upsetplot import from_contents, plot
from matplotlib import pyplot


def make_upset_plot(tasks: dict):

    data = {}
    for t in tasks:
        data[t] = list(tasks[t]["results"]["drugs"].keys())

    d = from_contents(data)
    plot(d)
    pyplot.show()
