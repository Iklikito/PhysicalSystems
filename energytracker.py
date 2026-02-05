import pygame
from constants import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT

pygame.init()
_font = pygame.font.SysFont("Consolas", 14)

class EnergyTracker:
    def __init__(self, max_time_span=10, plot_color=None, system=None, curve_thickness=None, plot_position=None, plot_width=None, plot_height=None):
        self.system = None
        if system != None: self.attach_to_system(system)
        self.energy_values = []
        self.max_time_span = max_time_span
        self.trajectory_colors = COLORS["white"] if plot_color is None else plot_color
        self.trajectory_thicknesses = 1 if curve_thickness is None else curve_thickness
        self.plot_position = plot_position
        self.plot_width = plot_width
        self.plot_height = plot_height

    def attach_to_system(self, new_system):
        if self.system == new_system:
            return
        
        self.system = new_system
        if new_system != None: new_system.attach_tracker(self)

    def get_new(self):
        return self.system.get_total_energy()

    def update(self, t):
        new_energy_value = self.get_new()
        self.energy_values.append([t, new_energy_value])
        while (self.energy_values[len(self.energy_values)-1][0] - self.energy_values[0][0] > self.max_time_span):
            self.energy_values.pop(0)

    def draw(self, screen):
        if self.plot_position is None: raise Exception("Energy tracker's plot position left unspecified.")
        if self.plot_width    is None: raise Exception("Energy tracker's plot width left unspecified."   )
        if self.plot_height   is None: raise Exception("Energy tracker's plot height left unspecified."  )

        if len(self.energy_values) < 2:
            return
        
        plot_rect = pygame.Rect(self.plot_position[0], self.plot_position[1], self.plot_width, self.plot_height)

        pygame.draw.rect(screen, COLORS["black"], plot_rect)
        pygame.draw.rect(screen, COLORS["white"], plot_rect, 1)

        t_min = self.energy_values[ 0][0]
        t_max = self.energy_values[-1][0]
        if t_max == t_min:
            t_max = t_min + max(self.max_time_span, 1e-6)

        energies = [pair[1] for pair in self.energy_values]
        e_min = min(energies)
        e_max = max(energies)
        if e_max == e_min:
            e_max = e_min + 1.0

        pad = 0.05 * (e_max - e_min)
        e_min -= pad
        e_max += pad

        points = []
        for t, e in self.energy_values:
            x = plot_rect.left + (t - t_min) / (t_max - t_min) * (plot_rect.width - 1)
            y = plot_rect.bottom - (e - e_min) / (e_max - e_min) * (plot_rect.height - 1)
            points.append((int(x), int(y)))

        pygame.draw.lines(
            screen,
            self.trajectory_colors,
            False,
            points,
            self.trajectory_thicknesses
        )

        t_min_text = _font.render(f"{t_min:.2f}", True, COLORS["white"])
        t_max_text = _font.render(f"{t_max:.2f}", True, COLORS["white"])
        e_min_text = _font.render(f"{e_min:.2f}", True, COLORS["white"])
        e_max_text = _font.render(f"{e_max:.2f}", True, COLORS["white"])

        screen.blit(t_min_text, (plot_rect.left, plot_rect.bottom + 2))
        screen.blit(t_max_text, (plot_rect.right - t_max_text.get_width(), plot_rect.bottom + 2))
        screen.blit(e_min_text, (plot_rect.left - e_min_text.get_width() - 4, plot_rect.bottom - e_min_text.get_height()))
        screen.blit(e_max_text, (plot_rect.left - e_max_text.get_width() - 4, plot_rect.top))
