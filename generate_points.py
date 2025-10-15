#!/usr/bin/env python3
import random
import csv

# Numero totale di punti (inclusi gli outlier)
TOTAL_POINTS = 5000

# Percentuale di outlier
OUTLIER_RATIO = 0.05  # 5%

# Cluster centrali (centroidi principali)
centers = [
    (1.0, 1.0),
    (5.0, 5.0),
    (9.0, 1.0),
    (5.0, 9.0),
    (1.0, 5.0)
]

# Deviazione standard (quanto sono “sparpagliati” i punti attorno al centro)
sigma = 0.3

# Calcola quanti outlier generare
num_outliers = int(TOTAL_POINTS * OUTLIER_RATIO)
num_normal = TOTAL_POINTS - num_outliers

# --------------------------
# Scrittura del file
# --------------------------
with open("points_with_outliers_5.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "x", "y", "label"])
    
    id_counter = 1
    
    # Genera punti normali attorno ai centroidi
    for cx, cy in centers:
        for _ in range(num_normal // len(centers)):
            x = random.gauss(cx, sigma)
            y = random.gauss(cy, sigma)
            writer.writerow([id_counter, round(x, 3), round(y, 3), "normal"])
            id_counter += 1

    # Genera outlier casuali in uno spazio più ampio
    for _ in range(num_outliers):
        x = random.uniform(-5, 15)
        y = random.uniform(-5, 15)
        writer.writerow([id_counter, round(x, 3), round(y, 3), "outlier"])
        id_counter += 1

print(f"✅ Generato file 'points_with_outliers.csv' con {TOTAL_POINTS} punti "
      f"({num_outliers} outlier).")
