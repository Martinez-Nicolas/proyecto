class Route:
    def __init__(self, path, cost):
        self.path = path  # List of vertices
        self.cost = cost

    def to_dict(self):
        return {
            "path": [str(v) for v in self.path],
            "cost": self.cost,
        }

    def __repr__(self):
        return f"Route(path={[v for v in self.path]}, cost={self.cost})"