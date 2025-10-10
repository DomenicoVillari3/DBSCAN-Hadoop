#!/usr/bin/env python
import sys
from collections import defaultdict, deque

# struttura dati: grafo di adiacenze
graph = defaultdict(set)

# --- Lettura input dallo STDIN ---
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        cell_a, cell_b = line.split('\t')
    except ValueError:
        continue
    graph[cell_a].add(cell_b)
    graph[cell_b].add(cell_a)  # connessione bidirezionale

# --- Ricerca componenti connesse ---
visited = set()
cluster_id = 0

for cell in graph:
    if cell in visited:
        continue

    cluster_id += 1
    queue = deque([cell])
    visited.add(cell)

    # BFS per esplorare il cluster
    while queue:
        current = queue.popleft()
        # stampa compatibile con python2/3
        print("{}\tcluster_{}".format(current, cluster_id))
        for neighbor in graph[current]:
            if neighbor not in visited and neighbor in graph:
                visited.add(neighbor)
                queue.append(neighbor)

