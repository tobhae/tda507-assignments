import math

target = 3.8
tolerance = 0.8

def dist(a, b):
    return math.dist(a, b)

def read_atoms(filename):
    atoms = []
    with open(filename) as f:
        for line in f:
            parts = line.split()
            atom_id = int(parts[0])
            x, y, z = map(float, parts[1:4])
            atoms.append([atom_id, (x, y, z), False])
    return atoms

def build_neighbour_list(atoms):
    n = len(atoms)
    nbrs = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            d = dist(atoms[i][1], atoms[j][1])
            if abs(d - target) < tolerance:
                nbrs[i].append(j)
                nbrs[j].append(i)
    return nbrs

def walk_chain(atoms, nbrs):
    n = len(atoms)

    # Find a chain endpoint (exactly 1 neighbour)
    start = None
    for i in range(n):
        if len(nbrs[i]) == 1:
            start = i
            break

    # Walk forward through the chain
    order = [start]
    prev = None
    current = start

    while True:
        neighbours = nbrs[current]
        next_atom = None
        for nb in neighbours:
            if nb != prev:
                next_atom = nb
                break
        if next_atom is None:
            break
        order.append(next_atom)
        prev, current = current, next_atom

    return order

if __name__ == "__main__":

    atoms = read_atoms("test_q1.txt")
    nbrs = build_neighbour_list(atoms)
    order = walk_chain(atoms, nbrs)
    for idx in order:
        print(atoms[idx][0])