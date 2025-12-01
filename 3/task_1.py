# Tobias Hägglund, tobhag@chalmers.se
# TDA507 assignment 3: Clustering proteins

import math
# Read file
def read_pdb(filename):
    models = []
    current_model = []

    with open(filename) as f:
        for line in f:
            if line.startswith("MODEL"):
                current_model = []
            
            elif line.startswith("ENDMDL"):
                models.append(current_model)

            elif line.startswith("ATOM") and " CA " in line:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                current_model.append((x, y, z))

    return models

def distance_matrix(coords):
    # Create matrix
    D = []  
    for i in range(len(coords)):
        row = []
        for j in range(len(coords)):
            row.append((0, 0))
        
        D.append(row)

    # Fill matrix
    for i in range(len(coords)):
        for j in range(len(coords)):
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            dz = coords[i][2] - coords[j][2]
            D[i][j] = math.sqrt(dx * dx + dy * dy + dz * dz)

    return D

def model_dist_score(D1, D2):
    total = 0.0

    for i in range(len(D1)):
        for j in range(i + 1, len(D1)):
            diff = D1[i][j] - D2[i][j]
            total += diff * diff

    return total

if __name__ == "__main__":
    models = read_pdb("4HIR.pdb")

    dist_mats = []
    for model in models:
        dist_mats.append(distance_matrix(model))

    best_score = float("inf")
    worst_score = -float("inf")
    best_pair = None
    worst_pair = None

    for i in range(len(models)):
        for j in range(i + 1, len(models)):
            score = model_dist_score(dist_mats[i], dist_mats[j])

            if score < best_score:
                best_score = score
                best_pair = (i + 1, j + 1)

            if score > worst_score:
                worst_score = score
                worst_pair = (i + 1, j + 1)
    
    print(f"Most similar pair: {best_pair}, with SSD: {best_score}")
    print(f"Most different pair: {worst_pair}, with SSD: {worst_score}")
    