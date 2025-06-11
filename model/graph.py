# graph.py
class Vertex:
    def __init__(self, label):
        self.label = label

    def element(self):
        return self.label

    def __repr__(self):
        return f"{self.label}"

    def __lt__(self, other):
        # Para heapq: compara por id, pero si los ids son iguales, compara por label
        if id(self) == id(other):
            return str(self.label) < str(other.label)
        return id(self) < id(other)

    def __eq__(self, other):
        if not isinstance(other, Vertex):
            return False
        return str(self.label) == str(other.label)

    def __hash__(self):
        return hash(str(self.label))

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
    
    def shortest_path(self, origin_label, destination_label):
        # Buscar los objetos Vertex correspondientes
        origin = None
        destination = None
        
        for v in self.vertices:
            if str(v.label) == origin_label:
                origin = v
            if str(v.label) == destination_label:
                destination = v
        
        if origin is None or destination is None:
            raise ValueError("Nodo origen o destino no encontrado")
        
        # Crear listas de adyacencia usando índices para evitar problemas de comparación
        n = len(self.vertices)
        vertex_list = self.vertices[:]  # Copia la lista
        
        # Buscar índices
        origin_idx = vertex_list.index(origin)
        destination_idx = vertex_list.index(destination)
        
        # Crear lista de adyacencia con índices
        adj_list = [[] for _ in range(n)]
        for edge in self.edges:
            try:
                from_idx = vertex_list.index(edge.origin)
                to_idx = vertex_list.index(edge.destination)
                adj_list[from_idx].append((to_idx, edge.cost))
            except ValueError:
                continue  # Saltar aristas con vértices no encontrados
        
        # Dijkstra usando solo índices
        import heapq
        dist = [float('inf')] * n
        prev = [None] * n
        visited = [False] * n
        
        dist[origin_idx] = 0
        heap = [(0, origin_idx)]
        
        while heap:
            d, u_idx = heapq.heappop(heap)
            if visited[u_idx]:
                continue
            visited[u_idx] = True
            
            if u_idx == destination_idx:
                break
            
            # Explorar vecinos usando la lista de adyacencia
            for v_idx, cost in adj_list[u_idx]:
                if visited[v_idx]:
                    continue
                if dist[u_idx] + cost < dist[v_idx]:
                    dist[v_idx] = dist[u_idx] + cost
                    prev[v_idx] = u_idx
                    heapq.heappush(heap, (dist[v_idx], v_idx))
        
        # Reconstruir camino
        if dist[destination_idx] == float('inf'):
            raise ValueError("No existe ruta entre los nodos seleccionados")
        
        path = []
        current_idx = destination_idx
        while current_idx is not None:
            path.insert(0, str(vertex_list[current_idx].label))
            current_idx = prev[current_idx]
        
        return path, dist[destination_idx]
