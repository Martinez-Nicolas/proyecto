import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

def plot_graph(graph, roles=None):
    G = nx.Graph()
    color_map = []
    for v in graph.vertices:
        G.add_node(str(v))
        if roles:
            if roles[v] == "storage":
                color_map.append("orange")
            elif roles[v] == "charge":
                color_map.append("cyan")
            elif roles[v] == "client":
                color_map.append("green")
            else:
                color_map.append("gray")
        else:
            color_map.append("gray")
    for e in graph.edges:
        G.add_edge(str(e.origin), str(e.destination), weight=e.cost)
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(7, 5))
    nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=700)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    st.pyplot(plt.gcf())
    plt.clf()