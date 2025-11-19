import math

target = 3.8
tolerance = 1.3

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
            atoms.append([atom_id, (x, y, z), False]) # False = unused
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

# Walking along the chain
def walk_chain(atoms, nbrs):
    n = len(atoms)
    start = None
    
    # Find a chain endpoint (exactly 1 neighbour)
    for i in range(n):
        if len(nbrs[i]) == 1:
            start = i
            break
    
    # Error handling
    if start is None:
        raise RuntimeError("No endpoint found")

    # Walk forward through the chain
    order = [start]
    prev = None
    current = start

    while True:
        neighbours = nbrs[current]
        next_atom = None

        for nb in neighbours: # Look at the neighbours of the current atom
            if nb != prev:
                next_atom = nb
                break

        if next_atom is None: # Final endpoint
            break

        order.append(next_atom)
        prev, current = current, next_atom

    return order

if __name__ == "__main__":
    atoms = read_atoms("test_q1.txt")
    nbrs = build_neighbour_list(atoms)
    order = walk_chain(atoms, nbrs)

    print(f"Reading test_q1.txt")
    print(f"Total number of alpha-carbons: {len(order)}")

    for idx in order:
        print(atoms[idx][0])

    atoms = read_atoms("data_q1.txt")
    nbrs = build_neighbour_list(atoms)
    order = walk_chain(atoms, nbrs)

    print(f"\nReading data_q1.txt")
    print(f"Total number of alpha-carbons: {len(order)}")

    for idx in order:
        print(atoms[idx][0])    