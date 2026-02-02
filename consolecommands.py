class ConsoleCommands():
    def __init__(self, commands={}):
        self.commands = commands

    def default_func(self, command_name):
        return command_name + " not recognized."

    def check_name_and_get(self, command_name, args):
        if command_name in self.commands:
            return self.commands[command_name][0](args)
        else:
            return self.default_func(command_name)

    def set(self, command_name, func, description=""):
        self.commands[command_name] = [func, description]

    def delete(self, command_name):
        self.commands.pop(command_name)