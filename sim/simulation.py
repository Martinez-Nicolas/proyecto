from domain.client import Client
from domain.order import Order
from domain.route import Route
from tda.avl import AVL

class Simulation:
    def __init__(self, graph):
        self.graph = graph
        self.clients = []
        self.orders = []
        self.routes_avl = AVL()

    def add_client(self, client):
        self.clients.append(client)

    def create_order(self, client, origin, destination, priority=1):
        order = Order(len(self.orders), client, origin, destination, priority)
        client.add_order(order)
        self.orders.append(order)
        return order

    def register_route(self, path, cost):
        # path como tupla de etiquetas
        key = "->".join([str(v) for v in path])
        self.routes_avl.root = self.routes_avl.insert(self.routes_avl.root, key)
        return key

    # Puedes agregar métodos de simulación, cálculo de rutas, etc.