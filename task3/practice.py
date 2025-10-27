
import os, sys
from collections import deque


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CH20_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "clrsPython", "Chapter20")
sys.path.insert(0, CH20_DIR)


class Queue:
    def __init__(self, capacity=0): self._q = deque()

    def enqueue(self, x): self._q.append(x)

    def dequeue(self): return self._q.popleft()

    def is_empty(self): return len(self._q) == 0


sys.modules["fifo_queue"] = type(sys)("fifo_queue")
sys.modules["fifo_queue"].Queue = Queue
sys.modules["adjacency_list_graph"] = type(sys)("adjacency_list_graph")
sys.modules["adjacency_list_graph"].AdjacencyListGraph = type("AdjacencyListGraph", (), {})
sys.modules["print_path"] = type(sys)("print_path")
sys.modules["print_path"].print_path = lambda pi, s, v, f: None

from bfs import bfs



class Edge:
    def __init__(self, v): self._v = v

    def get_v(self): return self._v


class Graph:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]

    def add_edge(self, u, v):
        self.adj[u].append(Edge(v))
        self.adj[v].append(Edge(u))

    def get_card_V(self): return self.n

    def get_adj_list(self, u): return self.adj[u]


def build_network():
    G = Graph(5)
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 3)]
    for u, v in edges:
        G.add_edge(u, v)
    return G


def get_path(pi, s, t):
    path = []
    v = t
    while v is not None:
        path.append(v)
        if v == s: break
        v = pi[v]
    return path[::-1]



stations = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
G = build_network()
dist, pi = bfs(G, 0)

path = get_path(pi, 0, 4)
print("Path:", " -> ".join(stations[i] for i in path))
print("Stops:", dist[4])











