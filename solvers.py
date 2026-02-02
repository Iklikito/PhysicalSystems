import numpy as np

class ExplicitEuler():
    def step(self, system, t, dt):
        state = system.state
        
        system.set_state(np.array([
            state[i] + dt*system.derivative_func(t, state)[i] for i in range(len(state))
        ]), t)

class ImplicitEuler():
    def step(self, system, t, dt):
        state = system.state
        # TODO

class RK4():
    def step(self, system, t, dt):
        state = system.state
        f = system.derivative_func
        
        k1 = dt*f(t,        state       )
        k2 = dt*f(t + dt/2, state + k1/2)
        k3 = dt*f(t + dt/2, state + k2/2)
        k4 = dt*f(t + dt,   state + k3  )

        system.set_state(np.array([
            state[i] + (1/6) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(state))
        ]), t)