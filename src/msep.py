"""
class creates multi species exclusion process.
"""

import numpy as np
import numba as nb
from itertools import combinations
import matplotlib.pyplot as plt

"""
monte carlo simulation with no just in time compiling.  
"""
@nb.njit 
def _jit_simulate(chain, rates_matrix, max_rate, steps):
    length = len(chain)
    history = np.zeros((steps + 1, length), dtype=chain.dtype)
    history[0] = chain.copy()
    
    current_chain = chain.copy()
    
    for step in range(1, steps + 1):
        i = np.random.randint(length)
        j = (i + 1) % length
        
        species_i = current_chain[i]
        species_j = current_chain[j]
        rate = rates_matrix[species_i, species_j]
        
        if np.random.rand() < rate / max_rate:
            current_chain[i], current_chain[j] = current_chain[j], current_chain[i]
            
        history[step] = current_chain.copy()
        
    return history

class MultiSpeciesExclusionProcess:
    def __init__(self, dimension, density, rates, length, shuffle=True):
        assert len(density) == dimension, "dimension-density mismatch"
        assert len(rates) == dimension * (dimension - 1), "rate-density mismatch"
        assert length%dimension == 0, "length-dimension mismatch"
        assert sum(density) == 1.0, "density not normalized"
        assert all(rate >= 0 for rate in rates.values()), "rates must be nonnegative"
        
        assert MultiSpeciesExclusionProcess.check_pairwise_balance(rates, dimension), "pairwise balance not imposed"

        self.dimension = dimension
        self.density = density
        self.rates = rates
        self.length = length
        self.proj_vectors = self.get_projected_vectors()

        self.chain = np.array([i for i, p in enumerate(self.density) for _ in range(int(p * self.length))])
        
        if shuffle:
            np.random.shuffle(self.chain)

    """
    note that this ensures the uniform distribution over all particle configurations 
    are an equilibrium/stationary distribution. 
    """
    @staticmethod
    def check_pairwise_balance(rates, dimension):
        species = range(dimension)

        for alpha, beta, gamma in combinations(species, 3):
            lhs = (rates[(alpha, beta)] + rates[(beta, gamma)] + rates[(gamma, alpha)])
            rhs = (rates[(beta, alpha)] + rates[(gamma, beta)] + rates[(alpha, gamma)])

            if not np.isclose(lhs, rhs):
                print("Balance failed for triple:", (alpha, beta, gamma))
                print("lhs =", lhs)
                print("rhs =", rhs)
                return False

        return True

    def get_projected_vectors(self):
        norm_vector = np.ones(self.dimension)
        n_hat = norm_vector / np.linalg.norm(norm_vector)
        I = np.eye(self.dimension)

        # Proj(v) = v - (v . n_hat) * n_hat
        projected_vectors = np.zeros((self.dimension, self.dimension))
        for i in range(self.dimension):
            e_i = I[i]
            projected_vectors[i] = e_i - np.dot(e_i, n_hat) * n_hat

        # Plane basis
        A = np.zeros((self.dimension, self.dimension))
        A[:, 0] = n_hat
        A[:, 1:] = np.random.randn(self.dimension, self.dimension - 1)

        q, r = np.linalg.qr(A)
        plane_basis = q[:, 1:]

        coords_2d = np.dot(projected_vectors, plane_basis)
        norms = np.linalg.norm(coords_2d, axis=1, keepdims=True)
        normalized_coords = np.divide(coords_2d, norms, out=np.zeros_like(coords_2d), where=norms!=0)

        return normalized_coords

    def simulate(self, steps=100000):
        rates_matrix = np.zeros((self.dimension, self.dimension), dtype=np.float64)
        for (i, j), rate in self.rates.items():
            rates_matrix[i, j] = rate
        self.max_rate = max(self.rates.values()) if self.rates else 1.0

        history = _jit_simulate(self.chain, rates_matrix, self.max_rate, steps)
        self.chain = history[-1].copy()

        return history

    def get_path(self):
        path = [np.zeros(self.dimension-1)]
        for x in self.chain:
            path.append(path[-1] + self.proj_vectors[x])
        return np.array(path)
    
    def get_chain(self):
        return self.chain
    
    @staticmethod
    def plot_path_2d(path):
        assert len(path[0]) == 2, "can only plot with dimension = 4"

        plt.figure(figsize=(6, 6))
        plt.plot(path[:, 0], path[:, 1], "-o", markersize=2)
        plt.axis("equal")
        plt.xlabel("h1")
        plt.ylabel("h2")
        plt.title("projected directed polymer path, d = 3")

        plt.show()

    @staticmethod
    def plot_path_3d(path):
        assert len(path[0]) == 3, "can only plot with dimension = 4"

        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection="3d")
        ax.plot(path[:, 0], path[:, 1], path[:, 2], "-o", markersize=2)
        ax.set_xlabel("h1")
        ax.set_ylabel("h2")
        ax.set_zlabel("h3")
        ax.set_title("projected directed polymer path, d = 4")
        ax.set_box_aspect([1, 1, 1])

        plt.show()
