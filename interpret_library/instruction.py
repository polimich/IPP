from interpret_library.util import *

# Classes for each arg_type

class Instruction:
    """ Class representing an instruction 
    
    Atributes:
    ----------
    
    stack : Stack
        stack for constants
    name : str
        name of the instruction
    order : int
        order of the instruction
    args : list
        list of arguments
    _frame_stack : FrameStack
        stack of frames
    _required_args : list
        list of required arguments
    _flow_manager : FlowManager
        flow manager
    
    """
    def __init__(self, name, order, args, frame_stack, flow_manager, stack) -> None:
        self.stack = stack
        self.name = name
        self.order = order
        self.args = args
        self._frame_stack = frame_stack
        self._required_args = []  # list of required args
        self._flow_manager = flow_manager

    def __repr__(self) -> str:
        return f"{self.name} {self.order} {self.args}"

    def _check_args(self):
        """ Checks if the arguments are correct"""
        if len(self.args) != len(self._required_args):
            exit(ErrorCodes.syntaxError)
        for arg, req_arg in zip(self.args, self._required_args):
            if isinstance(req_arg, list):
                is_correct = False
                for arg_type in req_arg:
                    if isinstance(arg, arg_type):
                        is_correct = True
                if not is_correct:
                    error("Incorrect argument in instruction", ErrorCodes.syntaxError)
            elif not isinstance(arg, req_arg):
                error("Incorrect argument in instruction", ErrorCodes.syntaxError)

    def exec(self):
        pass

    def get_symb_value(self, arg) -> Const:
        """ Returns value of symbol or variable"""
        if isinstance(arg, Var):
            return self._frame_stack.get_var_value(arg)
        else:
            return arg


class MOVE(Instruction):
    """ Class representing move instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const]]
        self._check_args()


    def exec(self):
        self._frame_stack.set_var(self.args[0], self.args[1])


class CREATEFRAME(Instruction):
    """ Class representing createframe instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = []
        self._check_args()

    def exec(self):
        self._frame_stack.create_frame()


class PUSHFRAME(Instruction):
    """ Class representing pushframe instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = []
        self._check_args()

    def exec(self):
        self._frame_stack.push_frame()


class POPFRAME(Instruction):
    """ Class representing popframe instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = []
        self._check_args()

    def exec(self):
        self._frame_stack.pop_frame()


class DEFVAR(Instruction):
    """ Class representing defvar instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var]
        self._check_args()

    def exec(self):
        self._frame_stack.def_var(self.args[0])


class CALL(Instruction):
    """ Class representing call instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Label]
        self._check_args()

    def exec(self):
        self._flow_manager.inst_stack.append(self._flow_manager.instruction_counter)
        found = False
        for label in self._flow_manager.label_dict.keys():
            if label == self.args[0].value:
                self._flow_manager.instruction_counter = self._flow_manager.label_dict[label]
                found = True
                break
        if not found:
            error(f"No such label {self.args[0].value}", ErrorCodes.semanticError)


class RETURN(Instruction):
    """ Class representing return instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = []
        self._check_args()

    def exec(self):
        try:
            self._flow_manager.instruction_counter = self._flow_manager.inst_stack.pop()
        except IndexError:
            error("No position in position stack", ErrorCodes.missingValueError)


# Stack instructions
class PUSHS(Instruction):
    """ Class representing pushs instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [[Var, Const]]
        self._check_args()

    def exec(self):
        self.stack.append(self.get_symb_value(self.args[0]))


class POPS(Instruction):
    """ Class representing pops instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var]
        self._check_args()

    def exec(self):
        try:
            self._frame_stack.set_var(self.args[0], self.stack.pop())
        except IndexError:
            error("Empty stack", ErrorCodes.missingValueError)

# Arithmetic instructions
class ADD(Instruction):
    """ Class representing add instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const], [Var, Const]]
        self._check_args()

    def exec(self):

        symb1 = self.get_symb_value(self.args[1])
        symb2 = self.get_symb_value(self.args[2])
        if symb1.type == int and symb2.type == int:
            self._frame_stack.set_var(self.args[0], Const("int", symb1.value + symb2.value))
        else:
            error("ADD: trying to add non integers", ErrorCodes.badTypeError)


class SUB(Instruction):
    """ Class representing sub instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const], [Var, Const]]
        self._check_args()

    def exec(self):

        symb1 = self.get_symb_value(self.args[1])
        symb2 = self.get_symb_value(self.args[2])
        if symb1.type == int and symb2.type == int:
            self._frame_stack.set_var(self.args[0], Const("int", symb1.value - symb2.value))
        else:
            error("SUB: trying to subtract non integers", ErrorCodes.badTypeError)


class MUL(Instruction):
    """ Class representing mul instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const], [Var, Const]]
        self._check_args()

    def exec(self):

        symb1 = self.get_symb_value(self.args[1])
        symb2 = self.get_symb_value(self.args[2])
        if symb1.type == int and symb2.type == int:
            self._frame_stack.set_var(self.args[0], Const("int", symb1.value * symb2.value))
        else:
            error("MUL: trying to add non integers", ErrorCodes.badTypeError)

# Logic instructions
class LT(Instruction):
    """ Class representing lt instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const], [Var, Const]]
        self._check_args()

    def exec(self):

        symb1 = self.get_symb_value(self.args[1])
        symb2 = self.get_symb_value(self.args[2])
        if symb1.type == symb2.type and symb1.type is not None:
            self._frame_stack.set_var(self.args[0], Const("bool", symb1.value < symb2.value))
        else:
            error("LT: trying to add non integers", ErrorCodes.badTypeError)


class GT(Instruction):
    """ Class representing gt instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const], [Var, Const]]
        self._check_args()

    def exec(self):
        symb1 = self.get_symb_value(self.args[1])
        symb2 = self.get_symb_value(self.args[2])
        if symb1.type == symb2.type and symb1.type is not None:
            self._frame_stack.set_var(self.args[0], Const('bool', symb1.value > symb2.value))
        else:
            error("GT: trying to add non integers", ErrorCodes.badTypeError)


class EQ(Instruction):
    """ Class representing eq instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const], [Var, Const]]
        self._check_args()

    def exec(self):
        symb1 = self.get_symb_value(self.args[1])
        symb2 = self.get_symb_value(self.args[2])
        if symb1.type == symb2.type or symb1.type is None or symb2.type is None:
            self._frame_stack.set_var(self.args[0], Const('bool', symb1.value == symb2.value))

        else:
            error("ADD: trying to add non integers", ErrorCodes.badTypeError)


class AND(Instruction):
    """ Class representing and instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const], [Var, Const]]
        self._check_args()

    def exec(self):
        symb1 = self.get_symb_value(self.args[1])
        symb2 = self.get_symb_value(self.args[2])

        if symb1.type == bool and symb2.type == bool:
            self._frame_stack.set_var(self.args[0], Const('bool', symb1.value and symb2.value))
        else:
            error("AND: bad type", ErrorCodes.badTypeError)


class OR(Instruction):
    """ Class representing or instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const], [Var, Const]]
        self._check_args()

    def exec(self):
        symb1 = self.get_symb_value(self.args[1])
        symb2 = self.get_symb_value(self.args[2])

        if symb1.type == bool and symb2.type == bool:
            self._frame_stack.set_var(self.args[0], Const('bool', symb1.value or symb2.value))
        else:
            error("OR: bad type", ErrorCodes.badTypeError)


class NOT(Instruction):
    """ Class representing not instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const]]
        self._check_args()

    def exec(self):
        symb1 = self.get_symb_value(self.args[1])

        if symb1.type == bool:
            self._frame_stack.set_var(self.args[0], Const('bool', not symb1.value))
        else:
            error("NOT: bad type", ErrorCodes.badTypeError)

# String instructions
class INT2CHAR(Instruction):
    """ Class representing int2char instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const]]
        self._check_args()

    def exec(self):
        symb1 = self.get_symb_value(self.args[1])

        if symb1.type == int:
            try:
                self._frame_stack.set_var(self.args[0], Const('string', chr(symb1.value)))
            except ValueError:
                error("INT2CHAR: bad string", ErrorCodes.badStringError)
        else:
            error("INT2CHAR: bad type", ErrorCodes.badTypeError)


class STRI2INT(Instruction):
    """ Class representing stri2int instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const], [Var, Const]]
        self._check_args()

    def exec(self):
        symb1 = self.get_symb_value(self.args[1])
        symb2 = self.get_symb_value(self.args[2])

        if symb1.type == str and symb2.type == int:
            try:
                self._frame_stack.set_var(self.args[0], Const('int', ord(symb1.value[symb2.value])))
            except IndexError:
                error("INT2CHAR: bad string", ErrorCodes.badStringError)
        else:
            error("INT2CHAR: bad types", ErrorCodes.badTypeError)

# IO instructions
class READ(Instruction):
    """ Class representing read instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, Type]
        self._check_args()

    def exec(self):
        if (read_type := self.args[1].value) == 'int':
            try:
                result = int(input())
            except ValueError:
                result = None
            except EOFError:
                result = None
        elif read_type == 'bool':
            try:
                if re.match(r'^true$', input(), re.IGNORECASE):
                    result = True
                else:
                    result = False
            except EOFError:
                result = None
        else:
            try:
                result = input()
            except EOFError:
                result = None

        if result is None:
            self._frame_stack.set_var(self.args[0], Const('nil', result))
        else:
            self._frame_stack.set_var(self.args[0], Const(read_type, result))


class WRITE(Instruction):
    """ Class representing write instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [[Var, Const]]
        self._check_args()

    def exec(self):
        if (symb := self.get_symb_value(self.args[0])).value is True:
            print('true', end="")
        elif symb.value is False:
            print('false', end="")
        elif symb.type in [str, int]:
            print(symb.value, end="")
        elif symb.type == 'nil':
            print("", end="")

# String instructions
class CONCAT(Instruction):
    """ Class representing concat instruction """
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const], [Var, Const]]
        self._check_args()

    def exec(self):
        symb1 = self.get_symb_value(self.args[1])
        symb2 = self.get_symb_value(self.args[2])

        if symb1.type == str and symb2.type == str:
            try:
                self._frame_stack.set_var(self.args[0], Const('string', symb1.value + symb2.value))
            except ValueError:
                error("CONCAT: bad string", ErrorCodes.badStringError)
        else:
            error("CONCAT: bad types", ErrorCodes.badTypeError)


class STRLEN(Instruction):
    """ Class representing strlen instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const]]
        self._check_args()

    def exec(self):
        symb1 = self.get_symb_value(self.args[1])
        if symb1.type == str:
            self._frame_stack.set_var(self.args[0],Const('int', len(symb1.value)))
        else:
            error("STRLEN: Bad type", ErrorCodes.badTypeError)


class GETCHAR(Instruction):
    """ Class representing getchar instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const], [Var, Const]]
        self._check_args()

    def exec(self):
        symb1 = self.get_symb_value(self.args[1])
        symb2 = self.get_symb_value(self.args[2])

        if symb1.type == str and symb2.type == int:
            try:
                self._frame_stack.set_var(self.args[0], Const('string', symb1.value[symb2.value]))
            except IndexError:
                error("GETCHAR: Index out of range", ErrorCodes.badStringError)
        else:
            error("GETCHAR: bad types", ErrorCodes.badTypeError)


class SETCHAR(Instruction):
    """ Class representing setchar instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const], [Var, Const]]
        self._check_args()

    def exec(self):
        var = self.get_symb_value(self.args[0])
        symb1 = self.get_symb_value(self.args[1])
        symb2 = self.get_symb_value(self.args[2])

        if symb1.type == int and symb2.type == str and var.type == str:
            var = list(var.value)
            try:
                var[symb1.value] = symb2.value[0]
                self._frame_stack.set_var(self.args[0],Const('string', ''.join(var)))
            except IndexError:
                error("SETCHAR: Index out of range", ErrorCodes.badStringError)
        else:
            error("SETCHAR: bad types", ErrorCodes.badTypeError)

# Type instructions
class TYPE(Instruction):
    """ Class representing type instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Var, [Var, Const]]
        self._check_args()

    def exec(self):
        symb1 = self.get_symb_value(self.args[1])
        if symb1.type == bool:
            self._frame_stack.set_var(self.args[0], Const('string', 'bool'))
        elif symb1.type == str:
            self._frame_stack.set_var(self.args[0], Const('string', 'string'))
        elif symb1.type == int:
            self._frame_stack.set_var(self.args[0], Const('string', 'int'))
        elif symb1.type is None and symb1.value == '':
            self._frame_stack.set_var(self.args[0], Const('string', ''))
        elif symb1.type is None:
            self._frame_stack.set_var(self.args[0], Const('string', 'nil'))

# Flow instructions
class LABEL(Instruction):
    """ Class representing label instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Label]
        self._check_args()

    def exec(self):
        label_dict = self._flow_manager.label_dict
        symb1 = self.get_symb_value(self.args[0])
        if symb1.value not in label_dict:
            label_dict[symb1.value] = self._flow_manager.instruction_counter
        else:
            error("LABEL: tried to create 2 identical labels", ErrorCodes.semanticError)


class JUMP(Instruction):
    """ Class representing jump instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Label]
        self._check_args()

    def exec(self):
        try:
            self._flow_manager.instruction_counter = self._flow_manager.label_dict[self.get_symb_value(self.args[0]).value]
        except KeyError:
            error("JUMP: jump to unknown label", ErrorCodes.semanticError)


class JUMPIFEQ(Instruction):
    """ Class representing jumpifeq instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Label, [Var, Const], [Var, Const]]
        self._check_args()

    def exec(self):
        label_dict = self._flow_manager.label_dict
        symb1 = self.get_symb_value(self.args[1])
        symb2 = self.get_symb_value(self.args[2])

        if symb1.type == symb2.type:
            if symb1.value == symb2.value:
                try:
                    self._flow_manager.instruction_counter = self._flow_manager.label_dict[
                        self.get_symb_value(self.args[0]).value]
                except KeyError:
                    error("JUMPIFEQ: jump to unknown label", ErrorCodes.semanticError)
        else:
            error("JUMPIFEQ: bad type", ErrorCodes.badTypeError)


class JUMPIFNEQ(Instruction):
    """ Class representing jumpifneq instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [Label, [Var, Const], [Var, Const]]
        self._check_args()

    def exec(self):
        label_dict = self._flow_manager.label_dict
        symb1 = self.get_symb_value(self.args[1])
        symb2 = self.get_symb_value(self.args[2])

        if symb1.type == symb2.type:
            if symb1.value != symb2.value:
                try:
                    self._flow_manager.instruction_counter = label_dict[
                        self.get_symb_value(self.args[0]).value]
                except KeyError:
                    error("JUMPIFEQ: jump to unknown label", ErrorCodes.semanticError)
        else:
            error("JUMPIFEQ: bad type", ErrorCodes.badTypeError)


class EXIT(Instruction):
    """ Class representing exit instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [[Var, Const]]
        self._check_args()

    def exec(self):
        symb1 = self.get_symb_value(self.args[0])
        if symb1.type == int:
            if 49 >= symb1.value >= 0:
                sys.exit(symb1.value)
            else:
                error("EXIT: bad error value", ErrorCodes.badOperandError)
        else:
            error("EXIT: bad error value", ErrorCodes.badTypeError)

# Debug instructions
class DPRINT(Instruction):
    """ Class representing dprint instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = [[Var, Const]]
        self._check_args()

    def exec(self):
        print(self.get_symb_value(self.args[0]), file=sys.stderr)


class BREAK(Instruction):
    """ Class representing break instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = []
        self._check_args()

    def exec(self):
        print(f"Position: {self._flow_manager.instruction_counter}\n"
              f"Frames: {self._frame_stack}", file=sys.stderr)

# Custom instructions
class LABEL_SUBSTITUTE(Instruction):
    """ Class representing label substitute instruction"""
    def __init__(self, name, order, args, frame_stack, flow_manager, stack):
        super().__init__(name, order, args, frame_stack, flow_manager, stack)
        self._required_args = []
        self._check_args()

    def exec(self):
        pass