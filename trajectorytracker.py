import pygame
from constants import COLORS

class TrajectoryTracker():
    def __init__(self, max_trajectory_lengths, trajectory_colors=[], system=None, trajectory_thicknesses=[]):
        self.system = None
        self.attach_to_system(system)
        self.N = len(max_trajectory_lengths)
        self.trajectories = [[] for _ in range(self.N)]
        self.max_trajectory_lengths = max_trajectory_lengths
        self.trajectory_colors = trajectory_colors if trajectory_colors != [] else [COLORS["white"]]*self.N
        self.trajectory_thicknesses = trajectory_thicknesses if trajectory_thicknesses != [] else [1]*self.N

    def attach_to_system(self, new_system):
        if self.system == new_system:
            return
        
        self.system = new_system
        new_system.attach_tracker(self)

    def update(self):
        new_positions = self.system.get_positions()
        
        for i in range(self.N):
            self.trajectories[i].append(new_positions[i])
            if len(self.trajectories[i]) > self.max_trajectory_lengths[i]:
                self.trajectories[i].pop(0)

    def draw(self, screen):
        for i in range(self.N):
            if len(self.trajectories[i]) < 2:
                continue

            pygame.draw.lines(
                screen,
                self.trajectory_colors[i],
                False,
                self.trajectories[i],
                self.trajectory_thicknesses[i]
            )