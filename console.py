import pygame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from consolecommands import ConsoleCommands
pygame.init()

font = pygame.font.SysFont("Consolas", 20)

class Console():
    def __init__(self, max_log_lines=7):
        self.input_text = ""
        self.log_lines = []
        self.max_log_lines = max_log_lines
        self.commands = ConsoleCommands()

    def set_command(self, command_name, func, parameter_types, description=""):
        self.commands.set(command_name, func, parameter_types, description)

    def add_to_input_text(self, char):
        self.input_text += char

    def delete_character(self):
        self.input_text = self.input_text[:-1]

    def add_log(self, output_text):
        self.log_lines.append(output_text)
        if len(self.log_lines) > self.max_log_lines:
            self.log_lines.pop(0)

    def run_command(self):
        if not self.input_text.strip():
            return
        
        parts = self.input_text.strip().split()
        command_name = parts[0 ]
        args =         parts[1:]

        new_log = self.commands.check_name_and_get(command_name, args)
        if new_log != None:
            self.add_log(new_log)
        self.input_text = ""

    def clear_logs(self):
        self.log_lines = []

    def draw(self, screen):
        CONSOLE_HEIGHT = WINDOW_HEIGHT // 3
        pygame.draw.rect(screen, (0, 0, 0), (0, WINDOW_HEIGHT - CONSOLE_HEIGHT, WINDOW_WIDTH, CONSOLE_HEIGHT))
        pygame.draw.rect(screen, (255, 255, 255), (0, WINDOW_HEIGHT - CONSOLE_HEIGHT, WINDOW_WIDTH, CONSOLE_HEIGHT), 2)

        for i, line in enumerate(self.log_lines):
            txt_surf = font.render(line, True, (255, 255, 255))
            screen.blit(txt_surf, (10, WINDOW_HEIGHT - CONSOLE_HEIGHT + 10 + i * 22))

        input_surf = font.render("> " + self.input_text, True, (0, 255, 0))
        screen.blit(input_surf, (10, WINDOW_HEIGHT - 30))