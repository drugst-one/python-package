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