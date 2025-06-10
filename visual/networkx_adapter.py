import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(graph):
    G = nx.Graph()
    for v in graph.vertices:
        G.add_node(str(v))
    for e in graph.edges:
        G.add_edge(str(e.origin), str(e.destination), weight=e.cost)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()