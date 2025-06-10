class Vertex:
    def __init__(self, label):
        self.label = label

    def element(self):
        return self.label

    def __repr__(self):
        return f"{self.label}"

class Edge:
    def __init__(self, origin, destination, cost):
        self.origin = origin
        self.destination = destination
        self.cost = cost

    def element(self):
        return self.cost

class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.vertices = []
        self.edges = []

    def insert_vertex(self, label):
        v = Vertex(label)
        self.vertices.append(v)
        return v

    def insert_edge(self, origin, destination, cost):
        e = Edge(origin, destination, cost)
        self.edges.append(e)
        if not self.directed:
            self.edges.append(Edge(destination, origin, cost))

    def neighbors(self, vertex):
        return [(e.destination, e.cost) for e in self.edges if e.origin == vertex]

    def get_edge(self, origin, destination):
        for e in self.edges:
            if e.origin == origin and e.destination == destination:
                return e
        return None
