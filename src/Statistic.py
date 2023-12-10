import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns

from src.Dijkstra import dijkstra_with_labels, dijkstra_fibonacci_heap
from src.Graph import generate_graph

sns.set_theme()


def collect_statistics(start_nodes, end_nodes, step, retry=1):
    '''The function runs two variation of Dijkstra algoritms and returns statistic of runs'''
    columns = ['Nodes', 'Time']

    labels_result = pd.DataFrame(columns=columns)
    heap_result = pd.DataFrame(columns=columns)

    for _ in range(retry):
        for n in range(start_nodes, end_nodes, step):
            g = generate_graph(n)

            labels_start = time.time()
            labels = dijkstra_with_labels(g, 0)
            labels_res = (time.time() - labels_start)

            heap_start = time.time()
            fib_heap = dijkstra_fibonacci_heap(g, 0)
            heap_res = (time.time() - heap_start)

            if labels != fib_heap:
                assert AssertionError(
                    "The results of the algorithms do not match"
                )

            labels_result.loc[len(labels_result.index)] = [n, labels_res]
            heap_result.loc[len(heap_result.index)] = [n, heap_res]

    labels_result = labels_result.groupby(by=columns[0]).mean().reset_index()
    heap_result = heap_result.groupby(by=columns[0]).mean().reset_index()

    return labels_result, heap_result


def plot_results(data1, data2, legend=['Labels', 'Fibonnacci heap'], xlabel='Number of nodes', ylabel='Time'):
    plt.plot(data1[data1.columns[0]],
             data1[data1.columns[1]], 'r')

    plt.plot(data2[data2.columns[0]],
             data2[data2.columns[1]], 'b')

    plt.legend(legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
