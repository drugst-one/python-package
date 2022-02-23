from matplotlib import pyplot as plt
from upsetplot import plot
from upsetplot import from_contents


def make_upset_plot():
    contents = {'cat1': ['a', 'b', 'c'],
                'cat2': ['b', 'd'],
                'cat3': ['e']}
    e = from_contents(contents)
    plot(e)
    plt.show()

# from upsetplotly import UpSetPlotly
#
#
# def make_upset_plot():
#     samples = [[1, 2, 3, 4], [2, 3, 4], [2, 5, 6]]
#     names = ["sample 1", "sample 2", "sample 3"]
#
#     usp = UpSetPlotly(samples=samples, sample_names=names)
#     usp.plot(order_by="decreasing")
