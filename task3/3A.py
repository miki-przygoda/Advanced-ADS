# task3/3a.py
"""
Task 3A: Tube Network Shortest Path (Toy Example)
Student: Tahzeeb Asif

This program finds the shortest path between stations A–E using
Breadth-First Search (BFS) from CLRS (Chapter 20).
"""

import os, sys

# === Setup CLRS library paths ===
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CLRS_ROOT = os.path.join(PROJECT_ROOT, "clrsPython")

sys.path.insert(0, CLRS_ROOT)
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter20"))
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter10"))
sys.path.insert(0, os.path.join(CLRS_ROOT, "UtilityFunctions"))

# Import CLRS BFS
from bfs import bfs

# === Graph Helper Classes ===

class Edge:
    """Simple edge class so CLRS BFS can read neighbours"""

    def __init__(self, v):
        self._v = v

    def get_v(self):
        return self._v


class Graph:
    """Undirected graph structure that matches CLRS BFS requirements"""

    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]

    def add_edge(self, u, v):
        self.adj[u].append(Edge(v))
        self.adj[v].append(Edge(u))

    def get_card_V(self):
        return self.n

    def get_adj_list(self, u):
        return self.adj[u]


def build_network():
    G = Graph(5)
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 3)]
    for u, v in edges:
        G.add_edge(u, v)
    return G


def get_path(pi, s, t):
    """Reconstruct the BFS shortest path"""
    path = []
    v = t
    while v is not None:
        path.append(v)
        if v == s:
            break
        v = pi[v]
    return path[::-1]


# === Run BFS ===

stations = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
G = build_network()

dist, pi = bfs(G, 0)  # BFS from A (0)
path = get_path(pi, 0, 4)  # A to E

print("=== Task 3A: Fewest Stops")
print("Path:", " -> ".join(stations[i] for i in path))
print("Stops:", dist[4])















