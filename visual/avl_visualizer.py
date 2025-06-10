import networkx as nx
import matplotlib.pyplot as plt

def add_edges(G, node, avl):
    if node:
        if node.left:
            G.add_edge(str(node.key), str(node.left.key))
            add_edges(G, node.left, avl)
        if node.right:
            G.add_edge(str(node.key), str(node.right.key))
            add_edges(G, node.right, avl)

def plot_avl(avl):
    G = nx.DiGraph()
    add_edges(G, avl.root, avl)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, arrows=True)
    plt.show()