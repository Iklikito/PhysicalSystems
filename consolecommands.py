from enum import Enum

class ParameterType(Enum):
    INT = 0
    FLOAT = 1
    STRING = 2

parameter_type_to_convert_func = {
    ParameterType.INT : int,
    ParameterType.FLOAT : float,
    ParameterType.STRING : str
}

class ConsoleCommands():
    def __init__(self, commands=None):
        self.commands = {} if commands is None else commands

    def default_func(self, command_name):
        return "Command \'" + command_name + "\' not recognized."

    def check_name_and_get(self, command_name, args):
        if command_name in self.commands:
            [func, parameter_types, description] = self.commands[command_name]

            if len(args) < len(parameter_types):
                return "Missing parameters."
            
            for i in range(len(parameter_types)):
                try:
                    args[i] = parameter_type_to_convert_func[parameter_types[i]](args[i])
                except:
                    return "Parameter " + str(i+1) + " should have type " + str(parameter_types[i])

            return func(args)
        else:
            return self.default_func(command_name)

    def set(self, command_name, func, parameter_types, description=""):
        self.commands[command_name] = [func, parameter_types, description]

    def delete(self, command_name):
        self.commands.pop(command_name)