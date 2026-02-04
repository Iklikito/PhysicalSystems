import numpy as np
import pygame
from constants import COLORS, g

class MultiPendulum:
    def __init__(self, thetas, thetadots, rod_lengths, masses, position, damping_coefficient=0.0):
        self.initial_thetas = thetas.copy()
        self.initial_thetadots = thetadots.copy()
        self.thetas = thetas.copy()
        self.thetadots = thetadots.copy()
        self.rod_lengths = rod_lengths
        self.masses = masses
        self.position = position
        self.damping_coefficient = damping_coefficient
        self.N = len(thetas)
        self.mass_suffix_sums = self.precompute_mass_suffix_sums()
        self.update_pendulum_positions()
        self.trackers = []

    @classmethod
    def single(cls, theta, thetadot, rod_length, mass, position, damping_coefficient=0.0):
        return cls(
            thetas=[theta],
            thetadots=[thetadot],
            rod_lengths=[rod_length],
            masses=[mass],
            position=position,
            damping_coefficient=damping_coefficient
        )
    
    @classmethod
    def double(cls, theta1, theta2, thetadot1, thetadot2, rod_length1, rod_length2, mass1, mass2, position, damping_coefficient=0.0):
        return cls(
            thetas=[theta1, theta2],
            thetadots=[thetadot1, thetadot2],
            rod_lengths=[rod_length1, rod_length2],
            masses=[mass1, mass2],
            position=position,
            damping_coefficient=damping_coefficient
        )

    def precompute_mass_suffix_sums(self):
        mass_suffix_sums = []
        current_sum = 0

        for i in range(self.N-1, -1, -1):
            current_sum += self.masses[i]
            mass_suffix_sums.append(current_sum)

        mass_suffix_sums.reverse()
        return mass_suffix_sums

    def derivative_func(self, t, state):
        N = self.N
        L = self.rod_lengths
        thetas    = state[:N]
        thetadots = state[N:]
        thetaddots = np.zeros(N)

        # --- See README for derivation ---
        A = np.zeros((N, N))
        b = np.zeros(N)

        for n in range(N):
            for j in range(N):
                mass_sum = self.mass_suffix_sums[max(j, n)]
                A[n][j] = mass_sum * L[j] * L[n] * np.cos(thetas[j] - thetas[n])
                if j == n:
                    b[n] += g * mass_sum * L[n] * np.cos(thetas[n])
                b[n] += mass_sum * L[j] * L[n] * thetadots[j] * thetadots[j] * np.sin(thetas[j] - thetas[n])

        undamped_thetaddots = np.linalg.solve(A, b)
        # --- See README for derivation ---

        thetaddots = undamped_thetaddots - self.damping_coefficient * thetadots

        return np.concatenate([thetadots, thetaddots])
    
    def update_pendulum_positions(self):
        self.pendulum_positions = []
        current_pendulum_position = self.position.copy()

        for i in range(self.N):
            current_pendulum_position[0] += self.rod_lengths[i] * np.cos(self.thetas[i])
            current_pendulum_position[1] += self.rod_lengths[i] * np.sin(self.thetas[i])
            self.pendulum_positions.append(current_pendulum_position.copy())

    def get_positions(self):
        return self.pendulum_positions

    def draw(self, screen):
        pygame.draw.line(
                screen,
                COLORS["white"],
                (             self.position[0],              self.position[1]),
                (self.pendulum_positions[0][0], self.pendulum_positions[0][1]),
                1
            )

        for i in range(self.N-1):
            pygame.draw.line(
                screen,
                COLORS["white"],
                (self.pendulum_positions[i  ][0], self.pendulum_positions[i  ][1]),
                (self.pendulum_positions[i+1][0], self.pendulum_positions[i+1][1]),
                1
            )

        for i in range(self.N):
            pygame.draw.circle(screen, COLORS["white"], self.pendulum_positions[i], 5)

    def get_state(self):
        return np.concatenate([self.thetas, self.thetadots])

    def get_initial_state(self):
        return np.concatenate([self.initial_thetas, self.initial_thetadots])

    def set_state(self, new_state, t):
        self.thetas = new_state[:self.N]
        self.thetadots = new_state[self.N:]
        self.update_pendulum_positions()
        self.update_trackers(t)

    def update_trackers(self, t):
        for tracker in self.trackers:
            tracker.update(t)

    def attach_tracker(self, tracker):
        if tracker in self.trackers:
            return

        self.trackers.append(tracker)

    def set_damping_coefficient(self, damping_coefficient):
        self.damping_coefficient = damping_coefficient