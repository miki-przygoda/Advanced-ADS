#Task 2B
#Oskar Kane
#27/10/25-

#Importing libraries
import sys, os, csv, random, time
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
clrs_dir = os.path.join(base_dir, "clrsPython")
for root, dirs, files in os.walk(clrs_dir):
    if root not in sys.path:
        sys.path.append(root)
from clrsPython.UtilityFunctions.adjacency_list_graph import AdjacencyListGraph
from clrsPython.Chapter22.dijkstra import dijkstra

#Choice on which dataset to run
choice_loop=True
creation_time=0
while choice_loop:
    choice=int(input("""Task 2b options:
1) Generate an artificial tube network
2) Use real world london underground dataset
Please enter 1 or 2: """))
    print("")
    #Artificial dataset
    if choice==1:
        print("Artificial tube network")
        #User input
        number_of_lines = int(input("Enter the number of lines: "))
        number_of_stations = int(input("Enter the number of stations per line: "))
        csv_file = os.path.join(os.path.dirname(__file__), "Generated_Test_Data.csv")
        start_creation = time.time()
        network = {}
        #Generate stations
        for line_num in range(1, number_of_lines + 1):
            line_name = f"Line{line_num}"
            stations = [f"{line_name}_Station{i}" for i in range(1, number_of_stations + 1)]
            network[line_name] = stations
        #Generate connections
        with open(csv_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            lines = list(network.keys())
            for line_name, stations in network.items():
                #Creates stations in a line
                for station in stations:
                    writer.writerow([line_name, station, "", ""])
                #Checks if line has one connection or not
                interlinked = False
                #Generates connections between stations
                for i in range(len(stations) - 1):
                    #Has a 40% chance of creating a linked station if not by halfway will create overlapping line
                    if (not interlinked and i == len(stations) // 2) or random.random() < 0.4:
                        #Picks a random line and station to connect to
                        other_line = random.choice([x for x in lines if x != line_name])
                        other_station = random.choice(network[other_line])
                        #Connects interchange stations on a line
                        duration_1 = random.randint(2, 6)
                        duration_2 = random.randint(2, 6)
                        writer.writerow([line_name, stations[i], other_station, duration_1])
                        writer.writerow([line_name, other_station, stations[i + 1], duration_2])
                        interlinked = True
                    else:
                        #Normal line connection
                        duration = random.randint(2, 6)
                        writer.writerow([line_name, stations[i], stations[i + 1], duration])
        end_creation=time.time()
        creation_time=end_creation - start_creation
        print(f"Total runtime to create dataset was {end_creation - start_creation} seconds")
        print("Artificial network has been saved to 'Generated_Test_Data.csv'")
        csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Generated_Test_Data.csv")
        choice_loop = False
    #London underground dataset
    elif choice==2:
        print("London tube network")
        csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), r"..\data\London_Underground_data.csv")
        choice_loop=False
    elif choice == 3:
        print("Test option to not change generated dataset")
        csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Generated_Test_Data.csv")
        choice_loop = False
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
vertex_to_index = {v: i for i, v in enumerate(stations)}
index_to_vertex = {i: v for v, i in vertex_to_index.items()}

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

start = time.time()

#Initilise empty weighted graph
G = AdjacencyListGraph(len(stations), weighted=True)
added_edges = set()

#Insert edges of both directions into the graph
for u, v, w in edges:
    u_idx = vertex_to_index[u]
    v_idx = vertex_to_index[v]
    edge_key = frozenset([u_idx, v_idx])
    if edge_key not in added_edges:
        G.insert_edge(u_idx, v_idx, w)
        G.insert_edge(v_idx, u_idx, w)
        added_edges.add(edge_key)

#Convert user input to indices for Dijkstra
source_idx = vertex_to_index[source]
target_idx = vertex_to_index[target]

#Runs Dijkstra
dist, parent = dijkstra(G, source_idx)

#Reformating the path from Dijkstra parent array
def get_path(parent, target_idx, index_to_vertex):
    path = []
    current = target_idx #Start
    visited = set()
    while current is not None and current not in visited: #Follows until source
        path.insert(0, index_to_vertex[current])
        visited.add(current)
        if parent[current] == current or parent[current] == -1:
            break
        current = parent[current]
    return path
path = get_path(parent, target_idx, index_to_vertex) #Get path

#Output of results
print(f"Shortest path from {source} to {target}: {' → '.join(path)}")
print(f"Total travel time: {dist[target_idx]} minutes")
end = time.time()
print(f"Search runtime is {end - start} seconds")
print(f"Total runtime of the whole program is {creation_time + (end - start)} seconds")