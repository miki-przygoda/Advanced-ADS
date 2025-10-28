"""
Task 4a — Core Backbone Network (Minimum Spanning Tree)
-------------------------------------------------------
This script uses CLRS library functions to compute the MST
for a small weighted network using Weighted Test Data.

Library components used:
- AdjacencyListGraph from clrsPython/UtilityFunctions/adjacency_list_graph.py
- mst_kruskal from clrsPython/Chapter21/mst.py

Algorithm complexity: O(E log V) (Kruskal's algorithm)
"""
from __future__ import annotations

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from clrsPython.UtilityFunctions.adjacency_list_graph import AdjacencyListGraph
from clrsPython.Chapter21.mst import kruskal

from task4.data_api import (
    _norm,               # Normalize station names
    init_index,          # BUILD the global index (loads CSV)
    get_all_stations,    # -> list[(id:int, name:str)]
    get_edge_info        # -> (time_minutes:int, line:str|None) or None
)

def build_graph_from_index() -> tuple[AdjacencyListGraph, dict[int, str]]:
    """
    Build an undirected, weighted CLRS graph using Task 1's station index.
    - Uses station IDs directly as CLRS vertex indices (0..N-1).
    - Inserts an undirected weighted edge once per pair (u < v).
    Returns: (graph, id_to_name)
    """
    # loads stations & edges once
    init_index()

    # Station listing: [(id, name), ...]
    stations = get_all_stations()   # e.g. [(0, 'Victoria'), (1, 'Oxford Circus'), ...]
    if not stations:
        # No stations loaded; return an empty graph
        return AdjacencyListGraph(card_V=0, directed=False, weighted=True), {}

    # Build ID<->Name maps (IDs are already stable from Task 1)
    id_to_name = {sid: sname for (sid, sname) in stations}
    station_ids = [sid for (sid, _name) in stations]
    n_vertices = max(station_ids) + 1  # IDs are 0..N-1 by construction in Task 1

    # Create weighted, undirected CLRS graph
    G = AdjacencyListGraph(card_V=n_vertices, directed=False, weighted=True)

    # Insert edges by scanning station pairs (u < v) and asking Task 1 for edge info
    # get_edge_info(name_u, name_v) returns (time_minutes, line) or None.
    names = [id_to_name[i] for i in range(n_vertices)]
    for u in range(n_vertices):
        name_u = names[u]
        for v in range(u + 1, n_vertices):
            name_v = names[v]
            info = get_edge_info(name_u, name_v)
            if info is None:
                continue
            time_minutes, _line = info
            # CLRS AdjacencyListGraph forbids parallel edges; Task 1 already keeps the min time.
            G.insert_edge(u, v, int(time_minutes))

    return G, id_to_name


def run_mst_demo():
    # Build CLRS graph directly from Task 1 data
    G, id_to_name = build_graph_from_index()

    # Compute MST (returns an AdjacencyListGraph that *is* the MST)
    mst_graph = kruskal(G)

    print("Minimum Spanning Tree (MST) edges:")
    total_weight = 0

    # For undirected graphs, get_edge_list() yields each edge once (u < v)
    for (u, v) in mst_graph.get_edge_list():
        e = mst_graph.find_edge(u, v)  # Edge object
        w = e.get_weight()
        total_weight += w
        # Use _norm to normalize station names for consistent display
        station_u = _norm(id_to_name.get(u, str(u)))
        station_v = _norm(id_to_name.get(v, str(v)))
        print(f"  {station_u} — {station_v}  (weight = {w})")

    print(f"\nTotal MST weight = {total_weight}")
    
    # Find maximum closable connections
    print("\nMaximum closable connections:")
    print("=" * 50)
    
    # Get all edges from original graph
    all_edges = []
    for u in range(G.card_V):
        for v in range(u + 1, G.card_V):
            edge = G.find_edge(u, v)
            if edge is not None:
                weight = edge.get_weight()
                station_u = _norm(id_to_name.get(u, str(u)))
                station_v = _norm(id_to_name.get(v, str(v)))
                all_edges.append((u, v, weight, station_u, station_v))
    
    # Get MST edges
    mst_edges = set()
    for (u, v) in mst_graph.get_edge_list():
        mst_edges.add((u, v))
        mst_edges.add((v, u))  # Add both directions
    
    # Find closable connections (edges not in MST)
    closable_connections = []
    for u, v, weight, station_u, station_v in all_edges:
        if (u, v) not in mst_edges and (v, u) not in mst_edges:
            closable_connections.append((u, v, weight, station_u, station_v))
    
    print(f"Total connections in network: {len(all_edges)}")
    print(f"Essential connections (MST): {len(mst_edges)//2}")
    print(f"Maximum closable connections: {len(closable_connections)}")
    
    if closable_connections:
        print(f"\nClosable connections (can be removed while maintaining connectivity):")
        for u, v, weight, station_u, station_v in closable_connections:
            print(f"  {station_u} — {station_v}  (weight = {weight})")
    else:
        print("No closable connections found - all connections are essential for connectivity.")


if __name__ == "__main__":
    run_mst_demo()