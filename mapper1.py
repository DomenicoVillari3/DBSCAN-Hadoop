

from math import floor
# import sys because we need to read and write data to STDIN and STDOUT
import sys


#epsilon : how much 2 points can be close to be considered in the same cluster
epsilon = 0.5

# reading entire line from STDIN (standard input)
for line in sys.stdin:
    if line.startswith("id"):
        continue  # Skip header line
    
    parts = line.strip().split(",")
    if len(parts) != 4:
        continue  # Skip malformed lines
    
    try:
        point_id = int(parts[0])
        x = float(parts[1])
        y = float(parts[2])
        label = parts[3]
    except ValueError:
        continue  # Skip lines with invalid data
    

    # Calcolo l’indice della cella
    cell_x = floor(x / epsilon)
    cell_y = floor(y / epsilon)
    #cell_id = (cell_x, cell_y,point_id)
    cell_id = str(cell_x)+","+str(cell_y)
    
    print("{},{}\t{}".format(cell_x, cell_y, 1))

