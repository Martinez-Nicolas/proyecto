import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

def add_edges(G, node):
    if node:
        if node.left:
            G.add_edge(str(node.key), str(node.left.key))
            add_edges(G, node.left)
        if node.right:
            G.add_edge(str(node.key), str(node.right.key))
            add_edges(G, node.right)

def plot_avl(avl):
    if not avl or not avl.root:
        st.info("AVL vacío.")
        return
    G = nx.DiGraph()
    add_edges(G, avl.root)
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 4))
    nx.draw(G, pos, with_labels=True, arrows=True, node_color="lightblue", node_size=800)
    st.pyplot(plt.gcf())
    plt.clf()