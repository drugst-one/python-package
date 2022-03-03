from upsetplot import from_contents, plot
from matplotlib import pyplot
from src.drugstone.task.task import Task


def make_upset_plot(tasks: list[Task]):

    data = []
    for t in tasks:
        data.append(list(t.get_result().get_drugs().keys()))

    # ex = from_memberships(data)
    ex = from_contents(
        {
            'cat1': ['a', 'b', 'c'],
            'cat2': ['b', 'd'],
            'cat3': ['e']
        }
    )

    plot(ex, orientation='vertical')
    pyplot.show()
