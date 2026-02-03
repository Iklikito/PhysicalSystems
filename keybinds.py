import pygame

class Keybinds:
    def __init__(self, init_key_to_func=None):
        self.key_to_func = {} if init_key_to_func is None else init_key_to_func

    def default_func(self, key):
        print("No function found. Key pressed:", str(key))

    def get(self, key):
        if key in self.key_to_func:
            self.key_to_func[key]()
        else:
            self.default_func(key)

    def set(self, key, func):
        self.key_to_func[key] = func

    def delete(self, key):
        self.key_to_func.pop(key, None)