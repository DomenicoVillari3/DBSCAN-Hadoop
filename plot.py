import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("output.txt", sep=r"\t", header=None,
                 names=["id", "x", "y", "label", "cluster"])

plt.figure(figsize=(8, 6))
for cluster, group in df.groupby("cluster"):
    plt.scatter(group["x"], group["y"], label=cluster)

plt.xlabel("x")
plt.ylabel("y")
plt.title("Cluster Visualization")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
