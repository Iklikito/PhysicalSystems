import pygame
import sys
import numpy as np
from keybinds import Keybinds
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS, CAPTION, dt
from dynamic_systems import SimplePendulum, DoublePendulum, MultiPendulum
from solvers import ExplicitEuler, RK4
from trajectorytracker import TrajectoryTracker
pygame.init()

key_binds = Keybinds()

def key_bind(char):
    def decorator(func):
        key_binds.set(pygame.key.key_code(char), func)
        return func
    return decorator

@key_bind("q")
def quit_game():
    global running
    running = False

@key_bind("s")
def toggle_simulation():
    global simulating
    simulating = not simulating

@key_bind("t")
def toggle_trajectories():
    global show_trajectories
    show_trajectories = not show_trajectories

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(CAPTION)

simple_pendulum = SimplePendulum(
    initial_state=np.array([-1.8, 0]), 
    rod_length=50, 
    position=[600,300],
    damping_coefficient=0.0625
)

double_pendulum = DoublePendulum(
    initial_state = np.array([0, 0, 0, 0]),
    rod_lengths=[100,50],
    masses=[1,1],
    position=[600,300],
    damping_coefficient=0.03125
)

multipendulum = MultiPendulum(
    initial_state=np.array([-1.5, -1.5, -1.5, -1.5, 0, 0, 0, 0]),
    rod_lengths=[100,50,25,12],
    masses=[1,1,1,1],
    position=[600,300],
    damping_coefficient=0.03125*0
)

multipendulum_trajectory_tracker = TrajectoryTracker(
    max_trajectory_lengths=[200]*4,
    trajectory_colors=[COLORS["gray"]]*4,
    system=multipendulum,
    trajectory_thicknesses=[1,2,4,8]
)

current_system = multipendulum
current_trajectory_tracker = multipendulum_trajectory_tracker

solver = RK4()
t = 0

simulating = False
show_trajectories = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            key_binds.get(event.key)

    if simulating:
        solver.step(current_system, t, dt)

    t += dt

    screen.fill(COLORS["black"])

    if show_trajectories:
        current_trajectory_tracker.draw(screen)

    current_system.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()