import pygame
from constants import COLORS

class TrajectoryTracker():
    def __init__(self, max_time_spans, trajectory_colors=None, system=None, trajectory_thicknesses=None):
        self.system = None
        if system != None: self.attach_to_system(system)
        self.N = len(max_time_spans)
        self.trajectories = [[] for _ in range(self.N)]
        self.max_time_spans = max_time_spans
        self.trajectory_colors = [COLORS["white"]]*self.N if trajectory_colors is None else trajectory_colors
        self.trajectory_thicknesses = [1]*self.N if trajectory_thicknesses is None else trajectory_thicknesses

    def attach_to_system(self, new_system):
        if self.system == new_system:
            return
        
        self.system = new_system
        if new_system != None: new_system.attach_tracker(self)

    def update(self, t):
        new_positions = self.system.get_positions()
        for i in range(self.N):
            self.trajectories[i].append([t, new_positions[i]])
            while self.trajectories[i][len(self.trajectories[i])-1][0] - self.trajectories[i][0][0] > self.max_time_spans[i]:
                self.trajectories[i].pop(0)

    def draw(self, screen):
        for i in range(self.N):
            if len(self.trajectories[i]) < 2:
                continue

            pygame.draw.lines(
                screen,
                self.trajectory_colors[i],
                False,
                [self.trajectories[i][j][1] for j in range(len(self.trajectories[i]))],
                self.trajectory_thicknesses[i]
            )