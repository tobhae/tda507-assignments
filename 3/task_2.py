# Tobias Hägglund, tobhag@chalmers.se
# TDA507 assignment 3: Clustering proteins

from task_1 import read_pdb, distance_matrix, model_dist_score
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

def plot_dendrogram():
    models = read_pdb("4HIR.pdb") # Read file

    # Compute distance matrices for each model
    distance_matrices = []
    for model in models:
        dm = distance_matrix(model)
        distance_matrices.append(dm)

    # Build SSD distance list
    distances = []
    for i in range(len(distance_matrices)):
        for j in range(i + 1, len(distance_matrices)):
            ssd = model_dist_score(distance_matrices[i], distance_matrices[j])
            distances.append(ssd)

    Z = linkage(distances, method="average")

    # Plot
    plt.figure(figsize=(12, 6))
    dendrogram(Z)
    plt.xlabel("Model number")
    plt.ylabel("Distance (SSD)")
    plt.title("Dendrogram")
    plt.show()

if __name__ == "__main__":
    plot_dendrogram()
