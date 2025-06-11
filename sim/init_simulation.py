from model.graph import Graph
from domain.client import Client
import random

def assign_roles(vertices, n_storage, n_charge, n_clients):
    """Assign roles to vertices: storage, charge, client"""
    roles = ["storage"] * n_storage + ["charge"] * n_charge + ["client"] * n_clients
    random.shuffle(roles)
    return dict(zip(vertices, roles))

def generate_random_graph(n_nodes, m_edges):
    graph = Graph(directed=False)
    vertices = []
    for i in range(n_nodes):
        v = graph.insert_vertex(f"N{i}")
        vertices.append(v)
    # Garantiza conexidad mínima
    for i in range(1, n_nodes):
        graph.insert_edge(vertices[i-1], vertices[i], random.randint(5, 15))
    # Aristas extra aleatorias
    added = n_nodes - 1
    while added < m_edges:
        u, v = random.sample(vertices, 2)
        if not graph.get_edge(u, v):
            graph.insert_edge(u, v, random.randint(5, 15))
            added += 1
    return graph, vertices

def generate_clients(vertices, roles):
    clients = []
    for v in vertices:
        if roles[v] == "client":
            clients.append(Client(str(v), f"Cliente_{str(v)}"))
    return clients