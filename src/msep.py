"""
class creates multi species exclusion process.
"""

import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt

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
        self.proj_vectors = self.get_proj_vectors()

        self.chain = np.array([i for i, p in enumerate(self.density) for _ in range(int(p * self.length))])
        assert len(self.chain) == self.length, "density does not produce correct chain length"
        
        if shuffle:
            np.random.shuffle(self.chain)

    """
    Note that this ensures the uniform distribution over all particle configurations 
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

    def get_proj_vectors(self):
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

    def monte_carlo_step(self):
        i = np.random.randint(len(self.chain))
        j = (i + 1) % len(self.chain)

        pair = (self.chain[i], self.chain[j])
        rate = self.rates.get(pair, 0.0)

        if np.random.rand() < rate / max(self.rates.values()):
            self.chain[i], self.chain[j] = self.chain[j], self.chain[i]

    def simulate(self, steps=5000):
        chains = [self.chain]
        for _ in range(steps):
            self.monte_carlo_step()
            chains.append(self.chain)

        return chains

    def get_path(self):
        path = [np.zeros(self.dimension-1)]
        for x in self.chain:
            path.append(path[-1] + self.proj_vectors[x])
        return np.array(path)
    
    def get_chain(self):
        return self.chain
    
    def plot_path_2d(self):
        assert self.dimension == 3, "can only plot with d = 3"
        path = self.get_path()

        plt.figure(figsize=(6, 6))
        plt.plot(path[:, 0], path[:, 1], "-o", markersize=2)
        plt.axis("equal")
        plt.xlabel("h1")
        plt.ylabel("h2")
        plt.title("projected directed polymer path, d = 3")
        plt.show()

    def plot_path_3d(self):
        assert self.dimension == 4, "can only plot with d = 4"
        path = self.get_path()

        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection="3d")
        ax.plot(path[:, 0], path[:, 1], path[:, 2], "-o", markersize=2)
        ax.set_xlabel("h1")
        ax.set_ylabel("h2")
        ax.set_zlabel("h3")
        ax.set_title("projected directed polymer path, d = 4")
        ax.set_box_aspect([1, 1, 1])

        plt.show()
