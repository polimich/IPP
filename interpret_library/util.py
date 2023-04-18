from interpret_library.error_codes import *
import re


class Var:
    """
    A class representing a variable

    Attributes:
    ----------
    frame_type : str
        type of the frame (GF, LF, TF)
    value : str
        name of the variable
    frame_stack : FrameStack
        stack of frames
    """

    def __init__(self, arg):
        if re.match(r"^(GF|LF|TF)@([a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*)$", arg):
            self.frame_type, self.name = arg.split("@")
        else:
            error("Invalid variable name", ErrorCodes.syntaxError)


class Const:
    def __init__(self, const_type: str, value: str):
        self.type, self.value = const_type, value
        if self.type == 'int' and re.match(r'^[+-]?[0-9]+$', self.value):
            self.value = int(self.value)
        elif self.type == 'bool' and re.match(r'^(true|false)$', self.value):
            if self.value == 'true':
                self.value = True
            else:
                self.value = False
        elif self.type == 'string' and not re.match(r'(\\[0-9]{0,2}($|[^0-9\\])|\\[0-9]{4,})', self.value, re.UNICODE):
            self.__replace_escape()
        else:
            error("Incorrect const type", ErrorCodes.syntaxError)

    def __replace_escape(self):
        """Replaces escape sequence with correct char"""
        pattern = re.compile(r'(\\[0-9]{3})', re.UNICODE)
        value = ''
        for part in pattern.split(self.value):
            if pattern.match(part):
                part = chr(int(part[1:]))
            value += part
        self.value = value


class Type:
    def __init__(self, value):
        if value == 'int':
            self.value = int
        elif value == 'string':
            self.value = str
        elif value == 'bool':
            self.value = bool
        elif value == 'nil':
            self.value = 'nil'
        else:
            error("Incorrect type", ErrorCodes.syntaxError)


class Label:
    def __init__(self, arg: str):
        if re.match(r'^[a-zA-Z_\-$&%*][a-zA-Z0-9_\-$&%*]*$', arg):
            self.value = arg
        else:
            error("Invalid Label", ErrorCodes.syntaxError)


class Frame:
    def __init__(self):
        self.g_frame = {}
        self.__frame_stack = []
        self.t_frame = None

    def create_frame(self):
        self.t_frame = {}

    def push_frame(self):
        if self.t_frame is not None:
            self.__frame_stack.append(self.t_frame)
            self.t_frame = None
        else:
            error("No TF defined", ErrorCodes.missingFrameError)

    def pop_frame(self):
        if len(self.__frame_stack):
            self.t_frame = self.__frame_stack.pop()

    def get_frame(self, frame: str) -> dict:
        """Returns frame """
        if frame == "GF":
            return self.g_frame
        elif frame == "LF":
            return self.get_local_frame()
        elif frame == "TF":
            return self.t_frame
        else:
            error(f"Frame not defined {frame}", ErrorCodes.missingFrameError)

    def get_local_frame(self):
        if len(self.__frame_stack) > 0:
            return self.__frame_stack[-1]
        else:
            error("No LF defined", ErrorCodes.missingFrameError)

    def def_var(self, var_name: str):
        if re.match(r"^(GF|LF|TF)@([a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*)$", var_name):
            frame, name = var_name.split("@")
            cur_frame = self.get_frame(frame)
            if name in cur_frame:
                error("Variable already exists", ErrorCodes.semanticError)
            else:
                cur_frame[name] = {'type': None, 'value': None}
        else:
            error("Bad var name", ErrorCodes.semanticError)

    def set_var(self, var: Var, symb):
        if re.match(r"^(GF|LF|TF)@([a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*)$", var.name):
            frame, name = var.name.split("@")
            cur_frame = self.get_frame(frame)
            if name in cur_frame:
                if isinstance(symb, Const):
                    cur_frame[name] = symb
                elif isinstance(symb, Var):
                    cur_frame[name] = self.get_var_value(symb)

            else:
                error(f"Undefined variable {var.name}", ErrorCodes.missingVarError)
        else:
            error("Bad var name", ErrorCodes.semanticError)

    def get_var_value(self, var: Var) -> int | bool | str:
        if re.match(r"^(GF|LF|TF)@([a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*)$", var.name):
            frame, name = var.name.split("@")
            cur_frame = self.get_frame(frame)
            if name in cur_frame:
                return cur_frame[name]
            else:
                error("Variable not defined in current frame addEC", ErrorCodes.missingVarError)

    def __repr__(self):
        return f"GF: {self.g_frame}\nLF: {self.get_local_frame() if len(self.__frame_stack) > 0 else ''} \nTF: {self.t_frame}"

class FlowManager:
    # Manages the state of Interpreter
    def __init__(self):
        self.instruction_counter = 0
        self.label_dict = {}
        self.inst_stack = []

