from math import sqrt
import networkx as nx
import requests
import scipy as sci
import numpy as num

graph = nx.read_gexf('./test.gexf')


def force_atlas_2(graph, k=1):

    position_map = {index: node for index, node in enumerate(graph.nodes_iter())}
    size = len(position_map)
    positions = num.random.random((size, 2)) - 0.5
    displacements = num.zeros((size, 2))
    adjacency_matrix = nx.to_numpy_matrix(graph)

    for x in range(1):
        for index, position in enumerate(positions):
            delta = (positions[index] - positions).T
            distance = num.sqrt((delta ** 2).sum(axis=0))
            distance = num.where(distance < 0.01, 0.01, distance)
            repulsion = (k / distance ** 2)


size = 1000
positions = num.array([[1, 2], [3, 4], [5, 6]])
force_atlas_2(graph)
