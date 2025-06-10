class Order:
    def __init__(self, order_id, client, origin, destination, priority=1):
        self.id = order_id
        self.client = client
        self.origin = origin
        self.destination = destination
        self.priority = priority
        self.status = "pending"
        self.created_at = None
        self.delivered_at = None
        self.cost = 0

    def __repr__(self):
        return f"Order({self.id}, {self.client.id}, from={self.origin}, to={self.destination})"