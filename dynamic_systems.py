from constants import g
import numpy as np
import pygame
from constants import COLORS

class MultiPendulum():
    def __init__(self, initial_state, rod_lengths, masses, position, damping_coefficient=0.0):
        self.initial_state = initial_state
        self.state = initial_state.copy()
        self.rod_lengths = rod_lengths
        self.masses = masses
        self.position = position
        self.damping_coefficient = damping_coefficient
        self.N = len(rod_lengths)
        self.mass_sums = self.precompute_mass_sums()
        self.update_pendulum_positions()
        self.trackers = []

    @classmethod
    def single(cls, initial_state, rod_length, mass, position, damping_coefficient=0.0):
        return cls(
            initial_state=initial_state,
            rod_lengths=[rod_length],
            masses=[mass],
            position=position,
            damping_coefficient=damping_coefficient
        )
    
    @classmethod
    def double(cls, initial_state, rod_length1, rod_length2, mass1, mass2, position, damping_coefficient=0.0):
        return cls(
            initial_state=initial_state,
            rod_lengths=[rod_length1, rod_length2],
            masses=[mass1,mass2],
            position=position,
            damping_coefficient=damping_coefficient
        )

    def precompute_mass_sums(self):
        mass_sums = []
        current_sum = 0

        for i in range(self.N-1, -1, -1):
            current_sum += self.masses[i]
            mass_sums.append(current_sum)

        mass_sums.reverse()
        return mass_sums

    def derivative_func(self, t, state):
        N = self.N
        result = np.zeros(2*N)

        for i in range(N):
            result[i] = state[i+N]

        A = np.zeros((N, N))
        b = np.zeros(N)

        for n in range(N):
            for j in range(N):
                A[n][j] = self.mass_sums[max(j, n)] * self.rod_lengths[j] * self.rod_lengths[n] * np.cos(state[j] - state[n])

        for n in range(N):
            b[n] = - g * self.mass_sums[n] * self.rod_lengths[n] * np.cos(state[n])
            for j in range(N):
                if j == n:
                    continue
                b[n] += self.mass_sums[max(j, n)] * self.rod_lengths[j] * self.rod_lengths[n] * state[j+N] * state[j+N] * np.sin(state[j] - state[n])

        undamped_thetadoubledots = np.linalg.solve(A, b)

        for i in range(N):
            result[i+N] = undamped_thetadoubledots[i] - self.damping_coefficient * state[i+N]

        return result
    
    def update_pendulum_positions(self):
        self.pendulum_positions = []
        current_pendulum_position = self.position.copy()

        for i in range(self.N):
            current_pendulum_position[0] += self.rod_lengths[i] * np.cos(self.state[i])
            current_pendulum_position[1] += self.rod_lengths[i] * np.sin(self.state[i])
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

    def set_state(self, new_state, t):
        self.state = new_state
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

    def get_initial_state(self):
        return self.initial_state