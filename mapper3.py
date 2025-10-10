#!/usr/bin/env python3
import sys
import re
from math import floor

epsilon = 0.5  # stesso valore usato nel primo job

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    # --- Caso 1: Riga del dataset originale (id,x,y,label) ---
    if line.count(",") == 3:
        parts = line.split(",")
        # Salta header
        if parts[0].lower() == "id":
            continue
        try:
            pid = parts[0]
            x = float(parts[1])
            y = float(parts[2])
            label = parts[3]
        except ValueError:
            continue  # scarta righe malformate

        cell_x = int(floor(x / epsilon))
        cell_y = int(floor(y / epsilon))
        cell_id = "{},{}".format(cell_x, cell_y)
        print("{}\tPOINT,{},{},{},{}".format(cell_id, pid, x, y, label))
        continue

    # --- Caso 2: Riga dal secondo job (celle clusterizzate) ---
    # Esempio: "7,11<TAB>cluster_1"
    parts = re.split(r'[\t ]+', line)
    if len(parts) == 2 and parts[1].startswith("cluster_"):
        cell_id = parts[0]
        cluster_id = parts[1]
        print("{}\tCLUSTER,{}".format(cell_id, cluster_id))
        continue

    # --- Caso 3: Formati misti o linee con spazi/virgole anomale ---
    tokens = re.split(r'[\t, ]+', line)
    if len(tokens) >= 2 and any("cluster_" in t for t in tokens):
        cell_id = ','.join([t for t in tokens if t.replace('-', '').isdigit()])
        cluster_id = next((t for t in tokens if t.startswith("cluster_")), None)
        if cell_id and cluster_id:
            print("{}\tCLUSTER,{}".format(cell_id, cluster_id))

