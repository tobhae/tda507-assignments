# Tobias Hägglund (tobhag@chalmers.se)
# TDA507 assignment 2: Main chain modelling
import math

target = 3.8
tolerance = 0.63

# Distance function
def dist(a, b):
    return math.dist(a, b)

# Reading the input
def read_atoms(filename):
    atoms = []

    with open(filename) as f:
        for line in f:
            parts = line.split()
            atom_id = int(parts[0])
            x, y, z = map(float, parts[1:4])
            atoms.append((atom_id, (x, y, z)))
    return atoms

# Building neighbor list
def build_neighbour_list(atoms):
    n = len(atoms)
    nbrs = []

    for i in range(n):      
        nbrs.append([]) # Init n empty lists, 1 neighbour list per atom

    for i in range(n):
        for j in range(i+1, n):
            d = dist(atoms[i][1], atoms[j][1])
            if abs(d - target) < tolerance: # If dist is good, connect both atoms
                nbrs[i].append(j)
                nbrs[j].append(i)
    return nbrs

# Depth-first search
def dfs(start, nbrs, visited):
    stack = [start]
    comp = []
    visited[start] = True

    while stack:
        v = stack.pop()
        comp.append(v)

        for nb in nbrs[v]:
            if not visited[nb]:
                visited[nb] = True
                stack.append(nb)

    return comp

# Walk from an endpoint or fallback to any node
def walk_chain(component, nbrs):

    # Find endpoints
    endpoints = []
    for i in component:
        if len(nbrs[i]) == 1:
            endpoints.append(i)

    if endpoints:
        current = endpoints[0]
    else:
        current = component[0]

    chain = []
    visited = set()
    prev = None

    while True:
        chain.append(current)
        visited.add(current)

        next_atom = None
        for nb in nbrs[current]:
            if nb != prev and nb not in visited: # Do not go backwards and do not revisit nodes
                next_atom = nb
                break

        if next_atom is None:
            break

        prev, current = current, next_atom

    return chain

# Run depth-first search on every unvisited node and use walk_chain on each component
def find_longest_chain(atoms, nbrs):
    visited = [False] * len(atoms)
    best_chain = []

    for i in range(len(atoms)):
        if not visited[i]:
            comp = dfs(i, nbrs, visited)
            chain = walk_chain(comp, nbrs)
            if len(chain) > len(best_chain):
                best_chain = chain

    return best_chain

if __name__ == "__main__":
    atoms = read_atoms("data_q2.txt")
    nbrs = build_neighbour_list(atoms)
    chain = find_longest_chain(atoms, nbrs)

    print(f"Reading data_q2.txt")
    print(f"Total number of alpha-carbons: {len(chain)}")

    for idx in chain:
        print(atoms[idx][0])