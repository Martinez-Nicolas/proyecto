class Route:
    def __init__(self, path, cost):
        self.path = path  # List of vertices
        self.cost = cost

    def __repr__(self):
        return f"Route(path={[v.element() for v in self.path]}, cost={self.cost})"