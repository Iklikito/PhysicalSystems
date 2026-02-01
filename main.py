import pygame
import sys
import numpy as np
from keybinds import Keybinds
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS, CAPTION, dt
from dynamic_systems import SimplePendulum, DoublePendulum
from solvers import ExplicitEuler, RK4
pygame.init()

def quit():
    global running
    running = False

def toggle_simulation():
    global simulating
    simulating = not simulating

key_binds = Keybinds(init_key_to_func={
    pygame.K_q : quit,
    pygame.K_s : toggle_simulation
})

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(CAPTION)

simple_pendulum = SimplePendulum(
    initial_state=np.array([-1.8, 0]), 
    rod_length=50, 
    position=[600,300],
    damping_coefficient=0.0625
)

double_pendulum = DoublePendulum(
    initial_state = np.array([0.1, 0.1, 0, 0]),
    rod_lengths=[50,50],
    masses=[1,1],
    position=[600,300],
    damping_coefficient=0.03125
)

current_system = double_pendulum

solver = RK4()
t = 0

simulating = False
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

    current_system.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()