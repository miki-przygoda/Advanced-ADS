# Task 3B Part 1 - Testing BFS speed on fake tube networks
# Student: Tahzeeb Asif
#
# In this part I'm checking how fast BFS runs when the network size increases.
# I reuse the BFS code from 3A (CLRS version).
# Then I make random "tube like" graphs and time BFS for different sizes.

import os, sys, random, time
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CLRS_ROOT = os.path.join(PROJECT_ROOT, "clrsPython")

sys.path.insert(0, CLRS_ROOT)
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter20"))
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter10"))
sys.path.insert(0, os.path.join(CLRS_ROOT, "UtilityFunctions"))

# CLRS BFS
from bfs import bfs

class Edge:
    def __init__(self, v):
        self._v = v
    def get_v(self):
        return self._v

class Graph:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
    def add_edge(self, a, b):
        # undirected edge
        self.adj[a].append(Edge(b))
        self.adj[b].append(Edge(a))
    def get_card_V(self):
        return self.n
    def get_adj_list(self, u):
        return self.adj[u]

# ---- make random graph like a tube map but fake ----
def build_random_graph(n, avg_degree=3):
    G = Graph(n)
    # each station connects to a few random stations
    for i in range(n):
        for _ in range(avg_degree):
            j = random.randint(0, n - 1)
            if j != i:
                G.add_edge(i, j)
    return G

# test time
def average_bfs_time(n, trials=30):
    G = build_random_graph(n)
    total = 0

    for _ in range(trials):
        s = random.randint(0, n - 1)
        t1 = time.time()
        bfs(G, s)   # using the CLRS bfs
        t2 = time.time()
        total += (t2 - t1)

    return total / trials

if __name__ == "__main__":
    sizes = [100,200,300,400,500,600,700,800,900,1000]
    times = []

    print("\n--- Task 3B Part 1: BFS Timing Test ---\n")

    for n in sizes:
        avg = average_bfs_time(n)
        times.append(avg)
        print(f"n = {n:4d} | avg BFS time = {avg:.6f} sec")

    # draw graph
    plt.plot(sizes, times, marker="o")
    plt.title("BFS Time vs Stations Count (Task 3B)")
    plt.xlabel("Number of Stations (n)")
    plt.ylabel("Average Time (seconds)")
    plt.grid(True)
    plt.show()

    print("\nBFS gets slower as n increases, roughly in a straight line")
    print("This matches BFS theory O(V + E)")

















