import numpy as np
from scipy.optimize import root

class ExplicitEuler():
    def step(self, system, t, dt):
        state = system.state
        f = system.derivative_func

        system.set_state(state + dt * f(t, state), t)

    def __str__(self):
        return "Explicit Euler"

class ImplicitEuler():
    def step(self, system, t, dt):
        state = system.state
        f = system.derivative_func

        def F(y):
            return y - state - dt*f(t + dt, y)

        system.set_state(root(F, state).x, t)

    def __str__(self):
        return "Implicit Euler"

class RK4():
    def step(self, system, t, dt):
        state = system.state
        f = system.derivative_func
        
        k1 = dt*f(t,        state       )
        k2 = dt*f(t + dt/2, state + k1/2)
        k3 = dt*f(t + dt/2, state + k2/2)
        k4 = dt*f(t + dt,   state + k3  )

        system.set_state(state + (1/6) * (k1 + 2 * k2 + 2 * k3 + k4), t)

    def __str__(self):
        return "RK-4"