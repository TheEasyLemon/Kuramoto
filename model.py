import numpy as np
import numpy.matlib as matlib

class Model:
    def __init__(self, N, K):
        self.N = N
        self.K = K

        # Inversely proportional to number of oscillators
        self.omega = (1 / N) * np.random.normal(0, 1, (N, 1))
        self.theta = np.zeros((N, 1))

        self.t = 0
        self.dt = 0.01

    def advance(self):
        internal_diff = matlib.repmat(self.theta, 1, self.N) - \
                        matlib.repmat(self.theta.T, self.N, 1)
        sync_factor = np.sum(np.sin(internal_diff), 1)
        sync_factor = sync_factor[..., None] # Promote to col vector

        dtheta_dt = self.omega + (self.K / self.N) * sync_factor
        self.theta = self.theta + dtheta_dt * self.dt
