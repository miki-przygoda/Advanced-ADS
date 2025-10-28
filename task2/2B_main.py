#Task 2B
#Oskar Kane
#27/10/25-

#Importing libraries
import sys, os, csv, random
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
clrs_dir = os.path.join(base_dir, "clrsPython")
for root, dirs, files in os.walk(clrs_dir):
    if root not in sys.path:
        sys.path.append(root)

from clrsPython.UtilityFunctions.adjacency_list_graph import AdjacencyListGraph
from clrsPython.Chapter22.dijkstra import dijkstra

#csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), r"..\data\London_Underground_data.csv")

choice_loop=True
while choice_loop:
    choice=int(input("""Task 2b options:
1) Generate an artificial tube network
2) Use real world london underground dataset
Please enter 1 or 2: """))
    if choice==1:
        # Ask user for input
        n_lines = int(input("Enter the number of lines: "))
        total_stations = int(input("Enter the total number of stations: "))
        output_file = "Generated_Test_Data.csv"

        # Calculate station distribution per line
        base_stations = total_stations // n_lines
        remainder = total_stations % n_lines

        # Data structures
        network = {}
        all_stations = {}

        station_counter = 1

        # --- Generate stations and line connections ---
        for line_num in range(1, n_lines + 1):
            line_name = f"Line{line_num}"
            num_stations = base_stations + (1 if line_num <= remainder else 0)

            # Create station names for this line
            stations = [f"{line_name}_Station{station_counter + i}" for i in range(num_stations)]
            station_counter += num_stations

            network[line_name] = stations
            all_stations[line_name] = stations

        # --- Write to CSV ---
        with open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            for line_name, stations in network.items():
                # Write all station names
                for station in stations:
                    writer.writerow([line_name, station, "", ""])

                # Write intra-line connections
                for i in range(len(stations) - 1):
                    duration = random.randint(2, 10)
                    writer.writerow([line_name, stations[i], stations[i + 1], duration])

            # --- Add at least one inter-line connection per line ---
            lines = list(network.keys())
            for i, line_name in enumerate(lines):
                other_line = random.choice([l for l in lines if l != line_name])
                station_a = random.choice(network[line_name])
                station_b = random.choice(network[other_line])
                duration = random.randint(3, 12)
                writer.writerow([line_name, station_a, station_b, duration])
        print(f"Tube network dataset successfully saved as '{output_file}'.")
        csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Generated_Test_Data")
        choice_loop=False
    elif choice==2:
        csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), r"..\data\London_Underground_data.csv")
        choice_loop=False
    else:
        print("Error: Invalid choice\n")

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

#Stations to search
loop=True
while loop:
    source = str(input("Please enter starting station name: "))
    target = str(input("Please enter ending station name: "))
    if source not in vertex_to_index and target not in vertex_to_index:
        print(f"Error: {source} and {target} are not in the data.\n")
    elif source not in vertex_to_index:
        print(f"Error: {source} is not in the data.\n")
    elif target not in vertex_to_index:
        print(f"Error: {target} is not in the data.\n")
    else:
        loop=False

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

#  Task 2B:Your shotest route will be of ===
print("=== Task 2B: Journey Planner ===\n")
print(f"Shortest path from {source} to {target}: {' → '.join(path)}")
print(f"Total travel time: {dist[target_idx]} minutes")
