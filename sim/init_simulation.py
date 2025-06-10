import random
from model.graph import Graph
from domain.client import Client

def generate_random_graph(n_nodes, m_edges):
    graph = Graph(directed=False)
    vertices = []
    for i in range(n_nodes):
        v = graph.insert_vertex(f"N{i}")
        vertices.append(v)
    # Conexión mínima para garantizar conexidad
    for i in range(1, n_nodes):
        graph.insert_edge(vertices[i-1], vertices[i], random.randint(1, 10))
    # Aristas aleatorias extra
    added = n_nodes - 1
    while added < m_edges:
        u, v = random.sample(vertices, 2)
        if not graph.get_edge(u, v):
            graph.insert_edge(u, v, random.randint(1, 10))
            added += 1
    return graph