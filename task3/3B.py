# Task 3B – London Underground BFS (Fewest Stops)
# Student: Tahzeeb Asif
# Using the same BFS from Task 3A but now with real stations

import os, sys, csv

# Set up CLRS paths same as in 3A
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CURRENT_DIR)
CLRS_PATH = os.path.join(ROOT, "clrsPython")

sys.path.insert(0, CLRS_PATH)
sys.path.insert(0, os.path.join(CLRS_PATH, "Chapter20"))
sys.path.insert(0, os.path.join(CLRS_PATH, "UtilityFunctions"))
sys.path.insert(0, os.path.join(CLRS_PATH, "Chapter10"))

from bfs import bfs


# Graph + Edge
class Edge:
    def __init__(self, v):
        self.v = v
    def get_v(self):
        return self.v


class Graph:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]

    def add_edge(self, a, b):
        self.adj[a].append(Edge(b))
        self.adj[b].append(Edge(a))

    def get_card_V(self):
        return self.n

    def get_adj_list(self, u):
        return self.adj[u]


# Load London Tube data
def load_tube_data():
    csv_path = os.path.join(ROOT, "data", "London_Underground_data.csv")

    stations = []
    edges = set()   # ✅ set avoids duplicate connections

    with open(csv_path, "r", encoding="utf-8") as f:
        read = csv.reader(f)
        for row in read:
            if len(row) < 3:
                continue
            s1 = row[1].strip()
            s2 = row[2].strip()
            if s1 != "" and s2 != "":
                stations.append(s1)
                stations.append(s2)
                edges.add((s1, s2))   # ✅ unique edge only

    stations = sorted(set(stations))
    name_to_id = {name: i for i, name in enumerate(stations)}

    G = Graph(len(stations))

    for s1, s2 in edges:
        a = name_to_id[s1]
        b = name_to_id[s2]
        G.add_edge(a, b)

    return G, stations, name_to_id


def build_path(parent, start, end):
    path = []
    x = end
    while x is not None:
        path.append(x)
        if x == start:
            break
        x = parent[x]
    return path[::-1]


# Run a journey
def run_route(G, stations, ids, start_name, end_name):
    if start_name not in ids or end_name not in ids:
        print("Station not found:", start_name, "or", end_name)
        return

    start = ids[start_name]
    end = ids[end_name]

    dist, parent = bfs(G, start)
    path = build_path(parent, start, end)

    station_names = [stations[p] for p in path]

    print("\nRoute:", start_name, "->", end_name)
    print("Path:", " -> ".join(station_names))
    print("Stops:", dist[end])


G, stations, ids = load_tube_data()

run_route(G, stations, ids, "Tottenham Hale", "Wimbledon Park")
run_route(G, stations, ids, "Baker Street", "Liverpool Street")




