#Task 2A
#Jeet Nadiapara
#20/10/25-27/10/25

#Importing libraries
import sys, os, csv
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
clrs_dir = os.path.join(base_dir, "clrsPython")
for root, dirs, files in os.walk(clrs_dir):
    if root not in sys.path:
        sys.path.append(root)

from clrsPython.UtilityFunctions.adjacency_list_graph import AdjacencyListGraph
from clrsPython.Chapter22.dijkstra import dijkstra

csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Weighted_Test_Data.csv")

edges = []
stations = set()

#Collecting data from csv file
with open(csv_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        #Expected column format- LineName, Station1, Station2, Time
        if len(row) < 4:
            continue
        line, s1, s2, weight = [r.strip() for r in row[:4]]
        if s1:
            stations.add(s1)
        if s2:
            stations.add(s2)
        try:
            weight = float(weight)
            edges.append((s1, s2, weight))
        except ValueError:
            pass

#buid graph
vertex_to_index = {v: i for i, v in enumerate(stations)}
index_to_vertex = {i: v for v, i in vertex_to_index.items()}

G = AdjacencyListGraph(len(stations), weighted=True)
added_edges = set()

min_edges = {}

for u, v, w in edges:
    u_idx = vertex_to_index[u]
    v_idx = vertex_to_index[v]

    # normalize key (undirected edge)
    key = tuple(sorted((u_idx, v_idx)))

    # keep the smaller weight if duplicates exist
    if key not in min_edges or w < min_edges[key]:
        min_edges[key] = w

# insert edges into graph (undirected)
for (u_idx, v_idx), w in min_edges.items():
    G.insert_edge(u_idx, v_idx, w)
    G.insert_edge(v_idx, u_idx, w)

#Stations to search
source = 'LineOne_One'
target = 'LineThree_Five'


if source not in vertex_to_index or target not in vertex_to_index:
    print(f"Error: Either {source} or {target} is missing in the CSV data.")
    sys.exit(1)

source_idx = vertex_to_index[source]
target_idx = vertex_to_index[target]

dist, parent = dijkstra(G, source_idx)

#reformating the path
def get_path(parent, target_idx, index_to_vertex):
    path = []
    current = target_idx
    visited = set()
    while current is not None and current not in visited:
        path.insert(0, index_to_vertex[current])
        visited.add(current)
        if parent[current] == current or parent[current] == -1:
            break
        current = parent[current]
    return path

path = get_path(parent, target_idx, index_to_vertex)

#  Task 2A:Your shotest route will be of ===
print("=== Task 2A: Journey Planner ===\n")
print(f"Shortest path from {source} to {target}: {' → '.join(path)}")
print(f"Total travel time: {dist[target_idx]} minutes")
