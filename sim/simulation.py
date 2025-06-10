from domain.order import Order
from domain.route import Route
from tda.avl import AVL

class Simulation:
    def __init__(self, graph, roles, clients):
        self.graph = graph
        self.roles = roles  # dict: vertex -> role
        self.clients = clients
        self.orders = []
        self.routes_avl = AVL()
        self.route_frequencies = {}

    def create_order(self, client, origin, destination, priority=1):
        order = Order(len(self.orders), client, origin, destination, priority)
        client.add_order(order)
        self.orders.append(order)
        return order

    def register_route(self, path, cost):
        key = "->".join([str(v) for v in path])
        if key in self.route_frequencies:
            self.route_frequencies[key] += 1
        else:
            self.route_frequencies[key] = 1
        self.routes_avl.root = self.routes_avl.insert(self.routes_avl.root, (key, self.route_frequencies[key]))
        return key

    def get_most_frequent_routes(self, top_n=10):
        sorted_routes = sorted(self.route_frequencies.items(), key=lambda x: -x[1])
        return sorted_routes[:top_n]