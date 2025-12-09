import numpy as np
import matplotlib.pyplot as plt

def read_trajectory(filename):
    return np.loadtxt(filename)

def discretize_uniform(x, n_bins=50):
    bins = np.linspace(x.min(), x.max(), n_bins + 1)
    symbols = np.digitize(x, bins) - 1
    symbols[symbols < 0] = 0
    symbols[symbols >= n_bins] = n_bins - 1

    return symbols

def calc_count_matrix(states, n_states):
    C = np.zeros((n_states, n_states), dtype=int)
    
    for a, b in zip(states[:-1], states[1:]):
        C[a, b] += 1

    return C
    
def calc_transition_matrix(C):
    n = C.shape[0]
    T = np.zeros((n, n), dtype=float)
    row_sums = C.sum(axis=1)

    for i in range(n):
        if row_sums[i] > 0:
            T[i] = C[i] / row_sums[i]
        
        else: 
            T[i, i] = 1.0

    return T

def calc_timescales(T, tau=1):
    eigenvalues, _ = np.linalg.eig(T)
    eigenvalues = np.real(eigenvalues)
    idx = np.argsort(-eigenvalues)      # Sort in descending order, largest -> slowest
    eigenvalues = eigenvalues[idx]

    print("Eigenvalue analysis:")
    print(f"Largest eigenvalue (stationary): λ_1 = {eigenvalues[0]:.6f}")

    timescales = []
    for i, lam in enumerate(eigenvalues[1:], start=2):
        if np.isclose(lam, 1.0):
            t = np.inf

        elif lam <= 0:
            t = np.nan
        
        else:
            t = -tau / np.log(lam)

        timescales.append(t)

        print(f"Eigenvalue {i}: λ = {lam:.6f}, timescale = {t}")

    return eigenvalues, np.array(timescales)

if __name__ == "__main__":
    traj = read_trajectory("traj-to-be-submitted.txt")
    symbols = discretize_uniform(traj, 50)

    # Plot 1D histogram
    plt.hist(symbols, bins=np.arange(51) - 0.5, edgecolor="black")
    plt.xlabel("Discrete state")
    plt.ylabel("Count")
    plt.title("1D plot discretized trajectory")
    #plt.show()

    C = calc_count_matrix(symbols, 50)
    print(f"Calculate matrix shape: {C.shape}")
    print(C, "\n")

    T = calc_transition_matrix(C)
    print(f"Transition matrix shape: {T.shape}\n")

    assert np.allclose(T.sum(axis=1), 1.0)      # Check that rows sum to one

    eigenvalues, timescales = calc_timescales(T, tau=1)