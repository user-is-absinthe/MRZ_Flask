import sys
import random
import os

from methods import func_read_from_csv as csv

import networkx
import matplotlib.pyplot
import numpy


def main():
    generate_matrix_in(64, '../data/true_chromatic/temp_matrix.txt')

    matrix_str = csv.open_matrix('../data/true_chromatic/temp_matrix.txt')

    if not csv.good_matrix(matrix_str):
        print('Bad matrix.')
        sys.exit(1)

    print(matrix_str)

    graph = create_graph(matrix_str)
    # print(graph.edges)
    draw_graph(graph)

    # new_graph = networkx.algorithms.coloring.greedy_color(graph)
    # print(new_graph)

    chromatic_number, colors = find_colors(graph)

    # draw_graph(graph, colors=colors, path_to_save='1.png')
    draw_graph(graph, colors=colors)

    pass


def get_path():
    return os.path.dirname(__file__)


def true_chromatic(path):
    matrix_str = csv.open_matrix(path)

    if not csv.good_matrix(matrix_str):
        # print('Bad matrix.')
        return 1

    graph = create_graph(matrix_str)

    draw_graph(graph)

    chromatic_number, colors = find_colors(graph)
    draw_graph(graph, colors=colors)

    return chromatic_number


def my_choice():
    # numpy.random.
    number = numpy.random.choice([0, 1], 1, p=[0.85, 0.15])
    return number[0]


def generate_matrix_in(size=2, path='data/true_chromatic/temp_matrix.txt'):
    with open(path, 'w') as file:
        for number_line in range(size):
            # line = [str(random.choice([0, 1])) for i in range(size)]
            line = [str(my_choice()) for i in range(size)]
            line_w = ''.join(line) + '\n'
            file.write(line_w)
    pass


def find_colors(graph):
    colors_dict = networkx.algorithms.coloring.greedy_color(graph)
    # keys = colors_dict.keys()
    color_scheme = colors_dict.values()
    color_scheme = list(set(color_scheme))
    for index in range(len(color_scheme)):
        color_scheme[index] = (random.random(), random.random(), random.random())
    colors = list()
    for node in graph.node:
        colors.append(color_scheme[colors_dict[node]])

    return len(color_scheme), colors


def create_graph(matrix_str):
    graph = networkx.Graph()
    graph.add_nodes_from([i + 1 for i in range(len(matrix_str))])
    for index_line in range(len(matrix_str)):
        for index_number in range(len(matrix_str[index_line])):
            if matrix_str[index_line][index_number] == '1':
                graph.add_edge(index_line + 1, index_number + 1)
    return graph


def draw_graph(graph, path_to_save=None, colors=None):
    position = networkx.shell_layout(graph)
    if colors is None:
        networkx.draw(graph, pos=position, with_labels=True)
    else:
        networkx.draw(graph, pos=position, node_color=colors, with_labels=True)
    if path_to_save is not None:
        matplotlib.pyplot.savefig(path_to_save, transparent=True)
    else:
        matplotlib.pyplot.show()
    matplotlib.pyplot.clf()
    pass


if __name__ == '__main__':
    main()
    # generate_matrix(10, '../data/true_chromatic/temp_matrix.txt')
