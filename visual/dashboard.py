import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from collections import Counter
import matplotlib.pyplot as plt
from domain.order import Order
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
        st.write(f"Tipo de objeto grafo: {type(st.session_state.graph)}")
        plot_graph(st.session_state.graph, st.session_state.roles)
        st.markdown("---")
        st.subheader("Calcular ruta más corta entre nodos")
        vertices = st.session_state.vertices
        vertex_names = [str(v) for v in vertices]
        origen = st.selectbox("Nodo origen", vertex_names, key="ruta_origen")
        destino = st.selectbox("Nodo destino", vertex_names, key="ruta_destino")
        if st.button("Calcular ruta más corta", key="btn_ruta_corta"):
            # Suponiendo que tu clase graph tiene un método shortest_path(origen, destino)
            try:
                path, cost = st.session_state.graph.shortest_path(origen, destino)
                st.success(f"Ruta más corta: {' → '.join(str(n) for n in path)} (Costo: {cost})")
            except Exception as e:
                st.error(f"No se pudo calcular la ruta: {e}")
    else:
        st.warning("Inicia una simulación primero.")

with tab3:
    st.header("Clientes y Órdenes")
    if st.session_state.sim:
        # --- CLIENTES ---
        st.subheader("Clientes activos")
        clientes = st.session_state.clients
        st.table([c.to_dict() for c in clientes])
        with st.expander("Agregar nuevo cliente"):
            nombre = st.text_input("Nombre", key="nuevo_cliente_nombre")
            prioridad = st.number_input("Prioridad", min_value=1, max_value=5, value=1, key="nuevo_cliente_prioridad")
            if st.button("Agregar Cliente", key="btn_agregar_cliente"):
                from proyecto.domain.client import Client
                nuevo = Client(len(clientes)+1, nombre, prioridad)
                clientes.append(nuevo)
                st.success(f"Cliente '{nombre}' agregado.")

        # --- ÓRDENES ---
        st.subheader("Órdenes")
        # Obtener las órdenes desde la simulación
        ordenes = getattr(st.session_state.sim, 'orders', [])
        if ordenes:
            st.table([o.to_dict() for o in ordenes])
        else:
            st.info("No hay órdenes registradas aún.")
        with st.expander("Agregar nueva orden"):
            cliente_sel = st.selectbox("Cliente", clientes, format_func=lambda c: c.name, key="orden_cliente_sel")
            origen = st.text_input("Origen", key="orden_origen")
            destino = st.text_input("Destino", key="orden_destino")
            prioridad = st.number_input("Prioridad", min_value=1, max_value=5, value=1, key="orden_prioridad")
            if st.button("Agregar Orden", key="btn_agregar_orden"):
                from proyecto.domain.order import Order
                nueva = Order(len(ordenes)+101, cliente_sel, origen, destino, prioridad)
                ordenes.append(nueva)
                cliente_sel.add_order(nueva)
                st.success(f"Orden agregada para {cliente_sel.name}.")
    else:
        st.warning("Inicia una simulación primero.")

with tab4:
    st.header("Rutas más frecuentes (AVL)")
    # --- RUTAS ---
    rutas = getattr(st.session_state.sim, 'routes', [])
    if rutas:
        st.table([r.to_dict() for r in rutas])
    else:
        st.info("No hay rutas registradas aún.")
    
with tab5:
    st.header("Estadísticas Generales")
    if st.session_state.sim:
        sim = st.session_state.sim
        roles = st.session_state.roles
        # --- Estadísticas de visitas basadas en órdenes ---
        ordenes = sim.orders if hasattr(sim, 'orders') else []
        nodos_visitados = []
        for o in ordenes:
            nodos_visitados.append(str(o.origin))
            nodos_visitados.append(str(o.destination))
        # Clasificar visitas por tipo de nodo
        clientes = [v for v in nodos_visitados if roles.get(next((x for x in roles if str(x)==v), None)) == 'client']
        recargas = [v for v in nodos_visitados if roles.get(next((x for x in roles if str(x)==v), None)) == 'charge']
        almacenamientos = [v for v in nodos_visitados if roles.get(next((x for x in roles if str(x)==v), None)) == 'storage']

        # --- Gráfico de barras: Clientes más visitados ---
        st.subheader("Nodos clientes más visitados")
        if clientes:
            c_counter = Counter(clientes)
            fig, ax = plt.subplots()
            ax.bar(c_counter.keys(), c_counter.values(), color='green')
            ax.set_xlabel('Nodo Cliente')
            ax.set_ylabel('Visitas')
            ax.set_title('Clientes más visitados')
            st.pyplot(fig)
        else:
            st.info("No hay visitas a nodos clientes.")

        # --- Gráfico de barras: Estaciones de recarga más visitadas ---
        st.subheader("Estaciones de recarga más visitadas")
        if recargas:
            r_counter = Counter(recargas)
            fig, ax = plt.subplots()
            ax.bar(r_counter.keys(), r_counter.values(), color='cyan')
            ax.set_xlabel('Estación de Recarga')
            ax.set_ylabel('Visitas')
            ax.set_title('Recargas más visitadas')
            st.pyplot(fig)
        else:
            st.info("No hay visitas a estaciones de recarga.")

        # --- Gráfico de barras: Nodos de almacenamiento más visitados ---
        st.subheader("Nodos de almacenamiento más visitados")
        if almacenamientos:
            a_counter = Counter(almacenamientos)
            fig, ax = plt.subplots()
            ax.bar(a_counter.keys(), a_counter.values(), color='orange')
            ax.set_xlabel('Nodo de Almacenamiento')
            ax.set_ylabel('Visitas')
            ax.set_title('Almacenamientos más visitados')
            st.pyplot(fig)
        else:
            st.info("No hay visitas a nodos de almacenamiento.")
    else:
        st.warning("Inicia una simulación primero.")