#!/usr/bin/env python
import sys

current_cell = None
cluster_id = None
points = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        cell, value = line.split('\t', 1)
    except ValueError:
        continue

    fields = value.split(',')

    if current_cell and cell != current_cell:
        # stampa i punti della cella precedente
        cid = cluster_id if cluster_id else "NOISE"
        for p in points:
            pid, x, y, label = p
            print("{}\t{}\t{}\t{}\t{}".format(pid, x, y, label, cid))
        # reset per la nuova cella
        points = []
        cluster_id = None

    current_cell = cell

    # tipo di record: CLUSTER o POINT
    record_type = fields[0]

    if record_type == "CLUSTER":
        if len(fields) > 1:
            cluster_id = fields[1]  # es. cluster_1
    elif record_type == "POINT":
        if len(fields) >= 5:
            pid, x, y, label = fields[1:]
            points.append((pid, x, y, label))

# stampa l'ultima cella
if current_cell:
    cid = cluster_id if cluster_id else "NOISE"
    for p in points:
        pid, x, y, label = p
        print("{}\t{}\t{}\t{}\t{}".format(pid, x, y, label, cid))

