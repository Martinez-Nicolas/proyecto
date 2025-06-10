class Client:
    def __init__(self, client_id, name, priority=1):
        self.id = client_id
        self.name = name
        self.priority = priority
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "priority": self.priority,
            "total_orders": len(self.orders),
        }

    def __repr__(self):
        return f"Client({self.id}, {self.name}, priority={self.priority})"