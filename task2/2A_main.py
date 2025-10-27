import sys, os, csv
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
clrs_dir = os.path.join(base_dir, "clrsPython")
for root, dirs, files in os.walk(clrs_dir):
    if root not in sys.path:
        sys.path.append(root)

# === Step 2: Import libraries ===
# These imports will work because we added all subdirectories
from clrsPython.UtilityFunctions.adjacency_list_graph import AdjacencyListGraph
from clrsPython.Chapter22.dijkstra import dijkstra

#importing the csv file
csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Weighted_Test_Data.csv")

edges = []
stations = set()

with open(csv_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        # Expected columns: LineName, Station1, Station2, Weight
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
vertex_to_index = {v: i for i, v in enumerate(sorted(stations))}
index_to_vertex = {i: v for v, i in vertex_to_index.items()}

G = AdjacencyListGraph(len(stations), weighted=True)
added_edges = set()

for u, v, w in edges:
    u_idx = vertex_to_index[u]
    v_idx = vertex_to_index[v]
    edge_key = frozenset([u_idx, v_idx])
    if edge_key not in added_edges:
        try:
            G.insert_edge(u_idx, v_idx, w)
            added_edges.add(edge_key)
        except RuntimeError:
            pass

#applying the dikstra algorithm
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
