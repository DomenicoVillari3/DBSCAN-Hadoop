#!/usr/bin/env python
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    if len(parts) < 3:
        continue  # cell_id, cell_type, count
    
    cell_id, cell_type, count = parts[0], parts[1], parts[2]
    if cell_type != "DENSE":
        continue  # consider only dense cells
    
    try:
        cx, cy = map(int, cell_id.split(","))
    except ValueError:
        continue
    
    # genera le celle adiacenti (8 vicine + se stessa)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx = cx + dx
            ny = cy + dy
            neighbor_id = "{},{}".format(nx, ny)
            
            # emetti relazione bidirezionale
            print("{}\t{}".format(cell_id, neighbor_id))

