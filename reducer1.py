#!/usr/bin/env python3
import sys

MinPts = 3  # soglia minima di densità

current_cell = None
count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    cell, val = line.split('\t')
    val = int(val)
    
    if current_cell == cell:
        count += val
    else:
        if current_cell is not None:
            # finito un gruppo: valuta densità
            if count >= MinPts:
                cell_type = "DENSE"
            else:
                cell_type = "SPARSE"
            print(f"{current_cell}\t{cell_type}\t{count}")
        
        current_cell = cell
        count = val

# ultima cella
if current_cell is not None:
    if count >= MinPts:
        cell_type = "DENSE"
    else:
        cell_type = "SPARSE"
    print(f"{current_cell}\t{cell_type}\t{count}")
