import pygame
import sys
import numpy as np
from keybinds import Keybinds
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS, CAPTION, dt, simulation_over_real_time_ratio, MAX_FPS
from dynamic_systems import MultiPendulum
from solvers import ExplicitEuler, ImplicitEuler, RK4
from trajectorytracker import TrajectoryTracker
from console import Console
from consolecommands import ParameterType
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

@key_bind("`")
def toggle_console():
    global console_open
    console_open = not console_open

@key_bind("r")
def reset():
    global current_system, t
    current_system.set_state(current_system.get_initial_state(), t)

console = Console()

def command(command_name, parameter_types, description=""):
    def decorator(func):
        console.set_command(command_name, func, parameter_types, description)
        return func
    return decorator

@command(command_name="echo", parameter_types=[ParameterType.STRING], description="Prints the first parameter back.")
def cmd_echo(args):
    return args[0]

@command(command_name="backgroundcolor", parameter_types=[ParameterType.STRING], description="Changes the background color to a predefined color.")
def cmd_bg_color(args):
    global background_color
    if args[0] not in COLORS:
        return "Color " + args[0] + " not recognized."
    background_color = COLORS[args[0]]
    return "Background color set to " + args[0] + "."

@command(command_name="backgroundrgb", parameter_types=[ParameterType.INT]*3, description="Changes the backgroudn color to the given rgb value.")
def cmb_bg_rgb(args):
    global background_color
    for i in range(3):
        if args[i] < 0 or args[i] > 255:
            return "Invalid rgb value."
    background_color = (args[0], args[1], args[2])
    return "Background rgb set to (" + str(args[0]) + ", " + str(args[1]) + ", " + str(args[2]) + ")."

@command(command_name="show", parameter_types=[ParameterType.STRING])
def cmd_show(args):
    global dt, current_system, current_solver
    variable_name_to_output = {
        "damping"  : "Damping coefficient: " + str(float(current_system.damping_coefficient)),
        "stepsize" : "Stepsize: " + str(dt),
        "solver"   : "Solver: " + str(current_solver)
    }
    if args[0] == "variablenames":
        return "Variable name list: " + str(list(variable_name_to_output.keys())) + "."
    if args[0] not in variable_name_to_output:
        return "Variable name not recognized."
    return variable_name_to_output[args[0]] + "."

@command(command_name="damping", parameter_types=[ParameterType.FLOAT])
def cmd_set_damping(args):
    global current_system
    current_system.set_damping_coefficient(args[0])
    return "Damping coefficient set to " + str(args[0])

@command(command_name="stepsize", parameter_types=[ParameterType.FLOAT])
def cmd_set_stepsize(args):
    global dt
    dt = args[0]
    return "Step size set to " + str(args[0])

@command(command_name="solver", parameter_types=[ParameterType.STRING])
def cmd_set_solver(args):
    global current_solver, exe_solver, ime_solver, rk4_solver
    solver_name_to_output = {
        "expliciteuler" : [exe_solver, "explicit euler"],
        "impliciteuler" : [ime_solver, "implicit euler"],
        "rk4"           : [rk4_solver, "RK-4"]
    }
    output = solver_name_to_output[args[0]]
    current_solver = output[0]
    return "Solver set to " + output[1] + "."

@command(command_name="reset", parameter_types=[])
def cmd_reset(args):
    global current_system, t
    current_system.set_state(current_system.get_initial_state(), t)
    return "System reset."

@command(command_name="quit", parameter_types=[])
def cmd_quit(args):
    global running
    running = False

multipendulum = MultiPendulum(
    initial_state=np.array([-1.5, -1.5, -1.5, -1.5, 0, 0, 0, 0]),
    rod_lengths=[100,50,25,12],
    masses=[1,1,1,1],
    position=[600,300],
    damping_coefficient=0.03125*0
)

multipendulum_trajectory_tracker = TrajectoryTracker(
    max_trajectory_lengths=[1]*4,
    trajectory_colors=[COLORS["gray"]]*4,
    system=multipendulum,
    trajectory_thicknesses=[1,2,4,8]
)

current_system = multipendulum
current_trajectory_tracker = multipendulum_trajectory_tracker

exe_solver = ExplicitEuler()
ime_solver = ImplicitEuler()
rk4_solver = RK4()
current_solver = rk4_solver
t = 0

background_color = COLORS["black"]

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()
accumulator = 0

simulating = False
show_trajectories = False
console_open = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if console_open:
                if event.key == pygame.K_RETURN:
                    console.run_command()
                elif event.key == pygame.K_BACKQUOTE:
                    console_open = False
                elif event.key == pygame.K_BACKSPACE:
                    console.delete_character()
                else:
                    console.add_to_input_text(event.unicode)
            else:
                key_binds.get(event.key)

    frame_time = simulation_over_real_time_ratio * clock.tick(MAX_FPS) / 1000

    if simulating:
        accumulator += frame_time

        while accumulator >= dt:
            current_solver.step(current_system, t, dt)
            t += dt
            accumulator -= dt

    screen.fill(background_color)

    if show_trajectories:
        current_trajectory_tracker.draw(screen)

    current_system.draw(screen)
    
    if console_open:
        console.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()