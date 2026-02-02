from constants import g
import numpy as np
import pygame
from constants import COLORS

class SimplePendulum():
    def __init__(self, initial_state, rod_length, position, damping_coefficient=0.0):
        self.state = initial_state
        self.rod_length = rod_length
        self.position = position
        self.damping_coefficient = damping_coefficient

    def derivative_func(self, t, state):
        return np.array([
            state[1],
            (-g / self.rod_length) * np.sin(state[0]) - self.damping_coefficient * state[1]
        ])
    
    def draw(self, screen):
        pendulum_position = [
            self.position[0] + self.rod_length * np.sin(self.state[0]),
            self.position[1] - self.rod_length * np.cos(self.state[0])
        ]
        pygame.draw.line(screen, COLORS["white"],
                         (    self.position[0],     self.position[1]),
                         (pendulum_position[0], pendulum_position[1]),
                         1)
        pygame.draw.circle(screen, COLORS["white"], pendulum_position, 5)

    def set_state(self, new_state):
        self.state = new_state

class DoublePendulum():
    def __init__(self, initial_state, rod_lengths, masses, position, damping_coefficient=0.0):
        self.state = initial_state
        self.rod_lengths = rod_lengths
        self.masses = masses
        self.position = position
        self.damping_coefficient = damping_coefficient

    def derivative_func(self, t, state):
        theta1    = self.state[0]
        theta2    = self.state[1]
        theta1dot = self.state[2]
        theta2dot = self.state[3]
        l1 = self.rod_lengths[0]
        l2 = self.rod_lengths[1]
        m1 = self.masses[0]
        m2 = self.masses[1]
        cos_thetadiff = np.cos(theta1 - theta2)
        sin_thetadiff = np.sin(theta1 - theta2)
        A = - m2 * l1 * l2 * cos_thetadiff
        B =   m2 * l1 * l1 * l2 * l2 * (m1 + m2 * sin_thetadiff * sin_thetadiff)
        C = - m2 * l1 * l2 * theta2dot * theta2dot * sin_thetadiff - (m1 + m2) * g * l1 * np.sin(theta1)
        D =   m2 * l1 * l2 * theta1dot * theta1dot * sin_thetadiff -       m2  * g * l2 * np.sin(theta2)
        return np.array([
            state[2],
            state[3],
            (1/B) * (m2 * l2 * l2 * C + A * D) - self.damping_coefficient * state[2],
            (1/B) * (A * C + (m1 + m2) * l1 * l1 * D) - self.damping_coefficient * state[3]
        ])
    
    def draw(self, screen):
        pendulum1_position = [
            self.position[0] + self.rod_lengths[0] * np.sin(self.state[0]),
            self.position[1] - self.rod_lengths[0] * np.cos(self.state[0])
        ]
        pendulum2_position = [
            pendulum1_position[0] + self.rod_lengths[1] * np.sin(self.state[1]),
            pendulum1_position[1] - self.rod_lengths[1] * np.cos(self.state[1])
        ]
        pygame.draw.line(
            screen,
            COLORS["white"],
            (     self.position[0],      self.position[1]),
            (pendulum1_position[0], pendulum1_position[1]),
            1
        )
        pygame.draw.line(screen, COLORS["white"],
            (pendulum1_position[0], pendulum1_position[1]),
            (pendulum2_position[0], pendulum2_position[1]),
            1
        )
        pygame.draw.circle(screen, COLORS["white"], pendulum1_position, 5)
        pygame.draw.circle(screen, COLORS["white"], pendulum2_position, 5)

    def set_state(self, new_state):
        self.state = new_state

class MultiPendulum():
    def __init__(self, initial_state, rod_lengths, masses, position, damping_coefficient=0.0):
        self.state = initial_state
        self.rod_lengths = rod_lengths
        self.masses = masses
        self.position = position
        self.damping_coefficient = damping_coefficient
        self.N = len(rod_lengths)
        self.mass_sums = self.precompute_mass_sums()
        self.update_pendulum_positions()
        self.trackers = []

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

    def set_state(self, new_state):
        self.state = new_state
        self.update_pendulum_positions()
        self.update_trackers()

    def update_trackers(self):
        for tracker in self.trackers:
            tracker.update()

    def attach_tracker(self, tracker):
        if tracker in self.trackers:
            return

        self.trackers.append(tracker)

    def set_damping_coefficient(self, damping_coefficient):
        self.damping_coefficient = damping_coefficient