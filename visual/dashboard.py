import streamlit as st

def main():
    st.title("Simulación de Drones - Correos Chile")
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Run Simulation", "Explore Network", "Clients & Orders", "Route Analytics", "General Statistics"
    ])
    with tab1:
        st.write("Aquí va la configuración y el inicio de la simulación.")
    with tab2:
        st.write("Visualización de red y cálculo de rutas.")
    with tab3:
        st.write("Listado de clientes y órdenes.")
    with tab4:
        st.write("Análisis de rutas (AVL).")
    with tab5:
        st.write("Estadísticas generales.")

if __name__ == "__main__":
    main()