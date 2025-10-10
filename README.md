# DBSCAN with Hadoop Streaming

This project implements a distributed version of **DBSCAN** (**Density-Based Spatial Clustering of Applications with Noise**) using **Hadoop Streaming** and **Python 3**.
The algorithm runs in 3 **MapReduce jobs**, operating on a 2-D dataset of points with a small percentage of outliers.

## **Project Structure**

```
.
├── mapper1.py       # Job 1 – Assign points to spatial cells
├── reducer1.py      # Job 1 – Compute cell density (DENSE / SPARSE)
├── mapper2.py       # Job 2 – Connect adjacent dense cells
├── reducer2.py      # Job 2 – Identify cluster groups
├── mapper3.py       # Job 3 – Assign original points to clusters
├── reducer3.py      # Job 3 – Produce final output (point → cluster_id)
├── generate.py       # Script that generates the synthetic dataset
├── points_with_outliers.csv   # Input dataset (CSV)
└── README.md
```

---

## **Dataset Generation**

Run the generator to create a dataset of 1,000 points (including 5 % outliers):

```bash
python3 generate.py
```

This produces a file `points_with_outliers.csv` with the following structure:

```
id,x,y,label
1,0.923,1.157,normal
2,5.124,4.987,normal
3,9.012,1.231,normal
...
1000,-4.123,12.433,outlier
```

---
## **Preparing the Input Directory in HDFS**

Before starting the MapReduce pipeline, create the HDFS input directory and upload the CSV dataset:

```bash
hdfs dfs -mkdir -p /user/root/input
hdfs dfs -put points_with_outliers.csv /user/root/input/
```

You can verify the upload with:

```bash
hdfs dfs -ls /user/root/input
```

Expected output:

```
Found 1 items
-rw-r--r--   1 root supergroup   12345  2025-10-10 14:00 /user/root/input/points_with_outliers.csv
```

---
## **Execution Workflow**

### **Job 1 – Cell Density Computation**

Each point is assigned to a cell defined as `(floor(x/ε), floor(y/ε))`.
The reducer counts how many points fall into each cell and marks it as **DENSE** or **SPARSE** depending on the threshold `MinPts`.

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming.jar \
  -input /user/root/input/points_with_outliers.csv \
  -output /user/root/output1 \
  -mapper "python3 mapper1.py" \
  -reducer "python3 reducer1.py" \
  -file mapper1.py \
  -file reducer1.py
```

**Output (`output1`):**

```
cell_id    DENSE/SPARSE    count
```

---

### **Job 2 – Cluster Formation**

This job identifies adjacent dense cells (sharing edges or corners) and groups them into clusters.

```bash
hadoop fs -rm -r -f /user/root/output2

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming.jar \
  -input /user/root/output1 \
  -output /user/root/output2 \
  -mapper "python3 mapper2.py" \
  -reducer "python3 reducer2.py" \
  -file mapper2.py \
  -file reducer2.py
```

**Output (`output2`):**

```
cell_id    cluster_id
```

Example:

```
7,11    cluster_1
8,10    cluster_1
9,11    cluster_1
```

---

### **Job 3 – Assign Points to Clusters**

Each original point from the CSV is mapped to the cluster of its corresponding cell.
If the cell does not belong to any cluster, the point is labeled as `NOISE`.

```bash
hadoop fs -rm -r -f /user/root/output3

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming.jar \
  -files mapper3.py,reducer3.py \
  -input /user/root/input/points_with_outliers.csv \
  -input /user/root/output2 \
  -output /user/root/output3 \
  -mapper "python3 mapper3.py" \
  -reducer "python3 reducer3.py"
```

**Output (`output3`):**

```
point_id    x     y     label     cluster_id
```

Example:

```
561   4.646   4.741   normal   cluster_1
565   4.821   4.705   normal   cluster_1
569   4.723   4.529   normal   cluster_1
977  -0.434  10.400   outlier  NOISE
```

---

