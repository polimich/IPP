# Author: Michael Polivka
# Login: xpoliv07
# Date: 5.4.2023 - xx.xx.xxxx
# Description: Interpret for IPPcode23 - ulitilities module


class Arg:
    def __init__(self, type, value ) -> None:
        self.type = type
        self.value = value
        
    def __repr__(self) -> str:
        return f"{self.type} {self.value}"
    
class Instruction:
    
    
    def __init__(self, name, number) -> None:
        self.name = name
        self.number = number
        self.args = []
        self._required_args = [] # list of required args
        
        
    def add_arg(self, arg) -> None:
        self.args.append(arg)
        
        
    def __repr__(self) -> str:
        return f"{self.name} {self.number} {self.args}"
    
    def _check(self, arg, type) -> bool:
        if arg.type == type:
            return True
        else:
            return False

class MOVE(Instruction):
    def __init__(self, name, number) -> None:
        super().__init__(name, number)
        self._required_args = ["var", "symb"]

class Frame():
    pass
    