import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from sim.init_simulation import generate_random_graph, assign_roles, generate_clients
from sim.simulation import Simulation
from visual.networkx_adapter import plot_graph
from visual.avl_visualizer import plot_avl
import json

# Estado global de la app
if "sim" not in st.session_state:
    st.session_state.sim = None
if "roles" not in st.session_state:
    st.session_state.roles = None
if "clients" not in st.session_state:
    st.session_state.clients = None
if "graph" not in st.session_state:
    st.session_state.graph = None
if "vertices" not in st.session_state:
    st.session_state.vertices = None

st.title("Simulación de Drones - Correos Chile")
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Run Simulation", "Explore Network", "Clients & Orders", "Route Analytics", "General Statistics"
])

with tab1:
    st.header("Configuración de la Simulación")
    n_nodes = st.slider("Número de nodos", 10, 150, 25)
    m_edges = st.slider("Número de aristas", n_nodes-1, min(300, (n_nodes*(n_nodes-1))//2), n_nodes*2)
    n_orders = st.slider("Número de órdenes", 10, 300, 30)

    st.info("Nodos: 20% almacenamiento, 20% recarga, 60% clientes")
    if st.button("📊 Start Simulation"):
        graph, vertices = generate_random_graph(n_nodes, m_edges)
        n_storage = n_nodes // 5
        n_charge = n_nodes // 5
        n_clients = n_nodes - n_storage - n_charge
        roles = assign_roles(vertices, n_storage, n_charge, n_clients)
        clients = generate_clients(vertices, roles)
        sim = Simulation(graph, roles, clients)
        st.session_state.sim = sim
        st.session_state.roles = roles
        st.session_state.clients = clients
        st.session_state.graph = graph
        st.session_state.vertices = vertices
        st.success("Simulación iniciada correctamente.")

with tab2:
    st.header("Visualización y Exploración de la Red")
    if st.session_state.graph:
        plot_graph(st.session_state.graph, st.session_state.roles)
    else:
        st.warning("Inicia una simulación primero.")

with tab3:
    st.header("Clientes y Órdenes")
    if st.session_state.sim:
        st.subheader("Clientes activos")
        st.json([c.to_dict() for c in st.session_state.clients])
        st.subheader("Órdenes")
        st.json([o.to_dict() for o in st.session_state.sim.orders])
    else:
        st.warning("Inicia una simulación primero.")

with tab4:
    st.header("Rutas más frecuentes (AVL)")
    if st.session_state.sim:
        st.subheader("Top rutas más frecuentes")
        st.json(st.session_state.sim.get_most_frequent_routes())
        plot_avl(st.session_state.sim.routes_avl)
    else:
        st.warning("Inicia una simulación primero.")

with tab5:
    st.header("Estadísticas Generales")
    if st.session_state.sim:
        # TODO: Agrega visualizaciones de estadísticas aquí
        st.info("Aquí irán las estadísticas globales del sistema.")
    else:
        st.warning("Inicia una simulación primero.")